import email
import traceback
from os import path

from flask import Blueprint, request

from ifsApprover import config
from ifsApprover.ImageActions import create_image_preview
from ifsApprover.Log import get_logger
from ifsApprover.Mail import send_new_image_mail
from ifsApprover.MailActions import make_unique_prefix, extract_and_store_image, make_db_entry
from ifsApprover.Utils import make_dirs_if_needed
from ifsApprover.web.helper import crossdomain


logger = get_logger("views/mails")

mails = Blueprint("mails", __name__)


@mails.route("/", methods=["POST"])
@crossdomain()
def new_mail():
    try:
        if not client_allowed():
            return "Client addres not allowd."

        raw_mail_str = request.values["mail"]

        prefix = make_unique_prefix()
        logger.info("New mail (%s)!" % prefix)

        mail_filename_full = path.join(config["MAIL_DIR"], "%s.mail" % prefix)
        image_name = "%s.jpg" % prefix
        image_filename_full = path.join(config["IMAGE_DIR"], image_name)

        make_dirs_if_needed(mail_filename_full)
        mail = email.message_from_string(raw_mail_str)
        # is this really an email?
        if mail["from"] is None:
            logger.error("Not a valid email.")
            return "No valid email"

        has_image = extract_and_store_image(mail, image_filename_full)
        if not has_image:
            make_db_entry(mail, None)
            logger.error("No attachment. (%s, %s)." % (mail["from"], mail["subject"]))
            return "No (jpeg) image found in the mail. Did you forget to attach the image?"

        image_size = create_image_preview(image_name)
        make_db_entry(mail, image_name, image_size)
        logger.info("Mail processing finished (%s, %s)." % (mail["from"], mail["subject"]))

        send_new_image_mail(mail["from"])

        return "OK!"

    except:
        logger.critical("An uncaught exception during mail receive: \n%s" % traceback.format_exc())
        return "Error :( \nPlease contact the admin."


def client_allowed():
    remote_addr = request.environ["REMOTE_ADDR"]
    allowed = remote_addr in config["MAIL_REQUESTS_FROM"]
    if not allowed:
        logger.warn("Client not allowed: %s" % remote_addr)
    return allowed