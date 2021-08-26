from os.path import join, dirname, abspath

_base_dir = abspath(dirname(__file__))

# _project_base_dir = join(_base_dir, "../")

LOG_DIR = join(_base_dir, "log")
CONSOLE_LOGGING = True

MAIL_REQUESTS_FROM = ["127.0.0.1", "172.17.0.1"]

DB_NAME = join(_base_dir, "database.db")
MAIL_DIR = join(_base_dir, "output", "mails")
IMAGE_DIR = join(_base_dir, "output", "images")

# serve static frontend
# you can disable this and serve the static content yourself
SERVE_STATIC_FRONTEND = True
STATIC_FRONTEND_DIR = join(_base_dir, "static-frontend")

# images
# (width, height) - in px
IMAGE_PREVIEW_SIZE = (500, 500)
IMAGEMAGICK_CONVERT = "/usr/bin/convert"
IMAGEMAGICK_IDENTIFY = "/usr/bin/identify"

#
APPROVED_IMAGE_DIR = "/ifs-backend/approved"
APPROVED_AFTER_ACTION = "ls"

MAIL_SUPPRESS_SEND = True
MAIL_SENDER = "ifs@kreativitaet-trifft-technik.de"
WEB_UI_URL = "http:/...."