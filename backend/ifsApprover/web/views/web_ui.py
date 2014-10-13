from flask import Blueprint, send_from_directory
from ifsApprover.web import app
from ifsApprover.web.helper import requires_auth

web_ui = Blueprint("web_ui", __name__)

folder = app.config["STATIC_FRONTEND_DIR"]

@app.route("/")
@requires_auth
def root():
    filename = "index.html"
    return send_from_directory(folder, filename)

@app.route("/<path:filename>")
@requires_auth
def path_file(filename):
    return send_from_directory(folder, filename)