from flask import Config
from os import path

config = Config('../')
config.from_object('config')

if path.exists(config["IMAGEMAGICK_CONVERT"]) is False:
    raise Exception("No imagemagick 'convert' found. Check your config or/and install imagemagick.")

from ifsApprover.Log import init_logger
init_logger()

from ifsApprover.DB import DB
db = DB(config["DB_NAME"])

