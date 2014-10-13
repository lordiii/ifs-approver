# -*- coding: utf8 -*-

from string import Template

from flask_mail import Mail, Message

from ifsApprover.Log import get_logger

from ifsApprover.web import app
from ifsApprover import db, config

#
# mail templates
#
NEW_IMAGE_MAIL = """\
Hallo,

$owner hat ein neues Image from Space hochgeladen.
    $url
Bitte prüfe es schalte es ggf. frei.


Viele Grüße,
IFS
"""

logger = get_logger("mail")
mail = Mail(app)


def send_new_image_mail(ifs_image_owner):
    msg = Message("New image from space", sender=config["MAIL_SENDER"])
    msg.charset = "utf8"

    login_list = map(lambda entry: entry["login"], db.get_users_list())

    msg.recipients = login_list
    msg.body = Template(NEW_IMAGE_MAIL).substitute(owner=ifs_image_owner, url=config["WEB_UI_URL"])
    logger.info("Sending new-image-mail (image from %s)" % ifs_image_owner)
    with app.app_context():
        mail.send(msg)
