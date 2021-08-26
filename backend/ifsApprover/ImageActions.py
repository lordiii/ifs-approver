import os
import re
from os import path
import shutil

from ifsApprover import db, Log, config
from ifsApprover.Mail import send_approve_mail, send_reject_mail
from ifsApprover.Utils import run


RE_IFS_JPG = re.compile("^([\d]{4})\.jpg")

logger = Log.get_logger("ImageActions")


def approve_image(image_id, user_login):
    logger.info("Approve image %s by %s." % (image_id, user_login))
    db.approve_image(image_id, user_login)
    image_data = db.get_single_image(image_id)
    _move_image_to_approve_dir(image_data["filename"])
    _run_after_approve()
    send_approve_mail(ifs_image_owner=image_data["sender"], image_filename=image_data["filename"], user_login=user_login)


def reject_image(image_id, user_login, reason):
    logger.info("Reject image %s by %s." % (image_id, user_login))
    db.reject_image(image_id, user_login, reason)
    image_data = db.get_single_image(image_id)
    send_reject_mail(ifs_image_owner=image_data["sender"], image_filename=image_data["filename"], reject_reason=reason, user_login=user_login)


def create_image_preview(image_filename):
    """
    Creates a preview image (size from config) for the given image name. It uses the configured image directory.
    :param image_filename: only the image filename, without any path!
    :return: the size (width, height) of the original image
    """
    logger.debug("Create image preview.")

    image_full_path = path.join(config["IMAGE_DIR"], image_filename)
    preview_full_path = path.join(config["IMAGE_DIR"], "preview_%s" % image_filename)

    # read size
    # http://www.imagemagick.org/script/escape.php
    cmd = "%s -format \"%%m,%%w,%%h\" %s" % (config["IMAGEMAGICK_IDENTIFY"], image_full_path)
    logger.debug("run: %s" % cmd)
    out = run(cmd, "identify")
    if "," not in out:
        raise Exception("Error getting size of %s. (identify output: '%s')" % (image_full_path, out))
    image_info = out.split(",")
    if image_info[0] != "JPEG":
        raise Exception("Image was not a JPEG, but '%s'. (identify output: '%s')" % (image_info[0], image_info))

    size_for_convert = "x".join(map(str, config["IMAGE_PREVIEW_SIZE"]))
    cmd = "%s %s -resize %s -auto-orient %s" % \
          (config["IMAGEMAGICK_CONVERT"], image_full_path, size_for_convert, preview_full_path)
    logger.debug("run: %s" % cmd)
    run(cmd, "convert")

    # removes the image type, only with/height remains
    image_info.pop(0)

    return image_info


def get_image_path(image_id, type='full'):
    image = db.get_single_image(image_id)
    if image is None:
        logger.warn("No image found for id %s" % image_id)
        return None
    if type == "preview":
        return path.join(config["IMAGE_DIR"], "preview_" + image["filename"])
    elif type == "full":
        status = image["status"]
        if status == db.STATUS_OK or status == db.STATUS_REJECTED:
            image_file = path.join(config["IMAGE_DIR"], image["filename"])
        else:
            return None
        if not path.exists(image_file):
            logger.warn("Expected image at '%s', but not found. Id: %s, type: %s" % (image_file, image_id, type))
            return None
        return image_file
    else:
        raise Exception("Invalid 'type' %s" % type)


def _move_image_to_approve_dir(image_filename):
    filename_with_path = path.join(config["IMAGE_DIR"], image_filename)
    target_folder = config["APPROVED_IMAGE_DIR"]

    # find last number
    max_number = 0
    for file in os.listdir(target_folder):
        match = RE_IFS_JPG.match(file)
        if match is None: continue
        max_number = max(max_number, int(match.group(1)))

    ifs_filename = "%04d.jpg" % (max_number + 1)
    shutil.move(filename_with_path, path.join(target_folder, ifs_filename))
    logger.debug("Image %s moved to %s", image_filename, ifs_filename)


def _run_after_approve():
    cmd = config["APPROVED_AFTER_ACTION"]
    logger.info("running APPROVED_AFTER_ACTION: %s" % cmd)
    out = run(cmd, "APPROVED_AFTER_ACTION")
    logger.debug(out)
