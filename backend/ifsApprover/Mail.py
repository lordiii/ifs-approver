# -*- coding: utf8 -*-
from string import Template

from flask_mail import Mail, Message

from ifsApprover import db, config
from ifsApprover.Log import get_logger
from ifsApprover.web import app

#
# mail templates
# (subject, body)
#

NEW_IMAGE_MAIL = (u"Neues IfS ($amount)!", u"""\
Hallo,

$owner hat ein neues Image from Space hochgeladen.
    $url

Bitte prüfe es schalte es ggf. frei.
Es gibt insgesamt $amount zu bearbeitende Bilder.

Viele Grüße,
IFS
""")

IMAGE_APPROVED = (u"Bild freigeschaltet :)", u"""\
Hallo,

dein Bild "$image" ist jetzt freigeschaltet.


Viele Grüße,
IFS
""")

IMAGE_REJECTED = (u"Bild zurückgewiesen :(", u"""\
Hallo,

dein Bild "$image" wurde NICHT freigeschaltet. Grund:
$reason


Viele Grüße,
IFS

""")

IMAGE_ACTION_ADMIN = (u"Bild $action ($amount)", u"""\
Hallo,

$admin hat das Bild "$image" von "$owner" bearbeitet. Ergebnis: $action
Es sind noch $amount Bilder offen.

Viele Grüße,
IFS

""")

logger = get_logger("mail")


def send_new_image_mail(ifs_image_owner):
    login_list = list(map(lambda entry: entry["login"], db.get_users_list()))
    image_pending = db.get_pending_images_count()

    subject = Template(NEW_IMAGE_MAIL[0]).substitute(amount=image_pending)
    body = Template(NEW_IMAGE_MAIL[1]).substitute(owner=ifs_image_owner, url=config["WEB_UI_URL"], amount=image_pending)

    logger.info("Sending new-image-mail (image from %s)" % ifs_image_owner)
    _send(recipients=login_list, subject=subject, body=body)


def send_approve_mail(ifs_image_owner, image_filename, user_login):
    body = Template(IMAGE_APPROVED[1]).substitute(image=image_filename)

    logger.info("Sending approve-mail (image %s from %s)" % (image_filename, ifs_image_owner))
    _send(recipients=[ifs_image_owner], subject=IMAGE_APPROVED[0], body=body)
    _send_other_admin_notification("APPROVED", ifs_image_owner, image_filename, user_login)


def send_reject_mail(ifs_image_owner, image_filename, reject_reason, user_login):
    body = Template(IMAGE_REJECTED[1]).substitute(image=image_filename, reason=reject_reason)

    logger.info("Sending reject-mail (image %s from %s)" % (image_filename, ifs_image_owner))
    _send(recipients=[ifs_image_owner], subject=IMAGE_REJECTED[0], body=body)
    _send_other_admin_notification("REJECT", ifs_image_owner, image_filename, user_login)


def _send_other_admin_notification(action, ifs_image_owner, image_filename, user_login):
    admins = db.get_users_list()
    other_admins = []
    for user in admins:
        if user["login"] == user_login.lower() or db.is_system_user(user):
            continue
        other_admins.append(user["login"])

    if len(other_admins) == 0:
        logger.info("There are no other admins to receive notification.")
        return

    image_pending = db.get_pending_images_count()
    subject = Template(IMAGE_ACTION_ADMIN[0]).substitute(action=action, amount=image_pending)
    body = Template(IMAGE_ACTION_ADMIN[1]).substitute(image=image_filename, owner=ifs_image_owner, admin=user_login, action=action,
                                                      amount=image_pending)
    logger.info("Sending notification to other admins (%s)" % other_admins)
    _send(recipients=other_admins, subject=subject, body=body)


def _send(recipients, subject, body):
    mail = Mail(app)
    msg = Message(subject, sender=config["MAIL_SENDER"])
    msg.charset = "utf8"
    msg.recipients = recipients
    msg.body = body
    with app.app_context():
        if config["MAIL_SUPPRESS_SEND"] is True:
            logger.debug(f"Mail (not sent):\n{msg}")
        else:
            mail.send(msg)
