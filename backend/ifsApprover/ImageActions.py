import os
import re
import subprocess
from os import path
import sys
import shutil

from ifsApprover import db, Log, config


RE_IFS_JPG = re.compile("^([\d]{4})\.jpg")

logger = Log.get_logger("ImageActions")


def approve_image(image_id, user_login):
    logger.info("Approve image %s." % image_id)
    db.approve_image(image_id, user_login)
    image_filename = db.get_image_filename(image_id)
    _move_image_to_approve_dir(image_filename)
    _run_after_approve()


def reject_image(image_id, user_login):
    db.reject_image(image_id, user_login)


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
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.read().rstrip()
    return_code = p.wait()
    if return_code != 0:
        raise StandardError("APPROVED_AFTER_ACTION failed. Log: \n%s" % out)
    logger.debug(out)
