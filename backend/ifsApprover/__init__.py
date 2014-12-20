from flask import Config
from os import path

config = Config('../')
config.from_object('config')

if path.exists(config["IMAGEMAGICK_CONVERT"]) is False:
    raise StandardError("No imagemagick 'convert' found. Check your config or/and install imagemagick.")

from ifsApprover.DB import DB
db = DB(config["DB_NAME"])

