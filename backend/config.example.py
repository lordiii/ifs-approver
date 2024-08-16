# copy this file to config.py

from os.path import join, dirname, abspath

_base_dir = abspath(dirname(__file__))

_project_base_dir = join(_base_dir, "../")

LOG_DIR = join(_project_base_dir, "log")
CONSOLE_LOGGING = False

MAIL_REQUESTS_FROM = ["127.0.0.1"]

DB_NAME = join(_project_base_dir, "ifs.db")
MAIL_DIR = join(_project_base_dir, "output", "mails")
IMAGE_DIR = join(_project_base_dir, "output", "images")

# serve static frontend
# you can disable this and serve the static content yourself
SERVE_STATIC_FRONTEND = True
STATIC_FRONTEND_DIR = join(_base_dir, "static-frontend")

# images
# (width, height) - in px
IMAGE_PREVIEW_SIZE = (500, 500)
IMAGEMAGICK_CONVERT = "convert"
IMAGEMAGICK_IDENTIFY = "identify"

#
APPROVED_IMAGE_DIR = "/tmp/your_path"
APPROVED_AFTER_ACTION = "echo YOUR COMMAND"

# mail
MAIL_SUPPRESS_SEND = True
MAIL_SENDER = "ifs@your-domain"
WEB_UI_URL = "https://your-domain-with-web-ui"

# GitHub Actions
GH_ENDPOINT = ""
GH_TOKEN = ""
GH_REF_BRANCH = "main"