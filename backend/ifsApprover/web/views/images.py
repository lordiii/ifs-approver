from flask import Blueprint, request

from ifsApprover.ImageActions import approve_image, reject_image

from ifsApprover.web.helper import requires_auth, copy_fields, make_json_response, crossdomain
from ifsApprover import db, DB


# logger = Log.get_logger("view/images")

images = Blueprint("images", __name__)


@images.route("/")
@crossdomain()
@requires_auth
def list_images():
    filter = request.args.get('filter')
    if filter is None or filter == "":
        images = db.get_pending_images()
    elif filter == "missing":
        images = db.get_missing_images()
    elif filter == "processed":
        images = db.get_processed_images()
    else:
        return make_json_response(status="Error: Unknown filter argument.")

    view_list = []
    for img_entry in images:
        view_list.append(copy_fields(img_entry, img_entry.keys()))

    return make_json_response(view_list)


@images.route("/<int:image_id>", methods=["PUT", "OPTIONS"])
@crossdomain()
@requires_auth
def update_image(image_id):
    status = request.json["status"]
    if status == DB.STATUS_APPROVED:
        approve_image(image_id, request.authorization.username)
    elif status == DB.STATUS_REJECTED:
        reason = request.json.get("reason")
        if reason is None:
            reason = "~ unknown ~"
        reject_image(image_id, request.authorization.username, reason)
    else:
        return make_json_response(status="Error: Invalid 'status' value.")

    return make_json_response()

