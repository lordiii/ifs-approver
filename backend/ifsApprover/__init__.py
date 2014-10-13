from flask import Config

config = Config('../')
config.from_object('config')

from ifsApprover.DB import DB
db = DB(config["DB_NAME"])

