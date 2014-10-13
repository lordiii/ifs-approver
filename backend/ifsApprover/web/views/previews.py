from flask import Blueprint, send_from_directory
from ifsApprover.web import app
from ifsApprover.web.helper import requires_auth, crossdomain

previews = Blueprint("previews", __name__)

@previews.route('/<path:filename>')
@crossdomain()
@requires_auth
def serve_images(filename):
    return send_from_directory(app.config["IMAGE_DIR"], filename)
