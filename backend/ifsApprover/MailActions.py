import sys
import time

from ifsApprover import db
from ifsApprover.Log import get_logger
from ifsApprover.Utils import make_dirs_if_needed, rnd_string

logger = get_logger("MailActions")


def get_first_matching_content_type(mail_mime_part, content_type_to_find):
    """
    Recursively searches all mime parts of the mail_mime_part until a jpeg attachment is found.
    :param mail_mime_part: part to start with
    :return: the part that represents the attachment or None
    """
    if not mail_mime_part.is_multipart():
        content_type = mail_mime_part.get_content_type()
        if content_type == content_type_to_find:
            return mail_mime_part
        return None

    for payload in mail_mime_part.get_payload():
        result = get_first_matching_content_type(payload, content_type_to_find)
        if result is not None:
            return result

    return None


def receive_and_store_mail(filename):
    """
    Receives the email content from stdin and stores it to the passed file. Returns also the content.
    :param filename:
    :return: the mail content
    """
    make_dirs_if_needed(filename)

    mail_data = []

    with open(filename, "wb") as fo:
        for line in sys.stdin:
            fo.write(line.encode())
            mail_data.append(line)

    logger.debug(f"Mail stored: {filename}")

    # the lines have already a line break
    return "".join(mail_data)


def extract_and_store_image(mail, image_filename_full):
    """
    Finds the (first) image from the parsed mail and stores it to image_filename.
    If the image is missing, None will be returned.
    :param mail:
    :param image_filename_full: the filename with full path
    :return: True for an image or False if missing
    """
    make_dirs_if_needed(image_filename_full)

    image_mime_part = get_first_matching_content_type(mail, "image/jpeg")
    if image_mime_part is None:
        return False

    with open(image_filename_full, "wb") as fo:
        fo.write(image_mime_part.get_payload(decode=True))

    logger.debug("Image stored: %s" % image_filename_full)

    return True



def make_db_entry(mail, image_file_name=None, image_size=None):
    plain_part = get_first_matching_content_type(mail, "text/plain")
    mail_body = plain_part.get_payload() if plain_part is not None else "~ no body ~"
    description = "Subject: %s\nBody:%s" % (mail["subject"], mail_body)

    if image_file_name is not None:
        db.add_image(mail["from"], description, image_file_name, image_size[0], image_size[1])
    else:
        db.add_no_image(mail["from"], description)


def make_unique_prefix():
    unix_timestamp = int(time.time())
    rnd = rnd_string(4)
    return "%s_%s" % (unix_timestamp, rnd)

