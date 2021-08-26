#!/usr/bin/env python3
import argparse
import getpass
import re
import sys
import os


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from ifsApprover import db

def set_or_add_user(login):
    print("Enter password for user '%s': " % login)
    password = getpass.getpass()
    if db.get_user_id(login) is None:
        print("Creating new user %s" % login)
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", login):
            print("Invalid login '%s'. Please use an email address as login." % login)
            return
        db.add_user(login, password)
    else:
        print("Updating password for %s" % login)
        db.update_password(login, password)


def list_users():
    print("id\tlogin")
    print("--\t-----")
    for u in db.get_users_list():
        print("%s\t%s" % (u["id"], u["login"]))


def list_images():
    print("# Images:")
    for entry in db.get_pending_images():
        print(entry)

    missing = db.get_missing_images()
    if len(missing) > 0:
        print("# Missing images:")
        for entry in missing:
            print(entry)

    print("# Approved or rejected")
    for entry in db.get_processed_images():
        print(entry)


def update_image_status(id, status):
    db.update_image_by_system(id, status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='db utils')
    subparsers = parser.add_subparsers(help='sub-command help', dest="sub")

    subparsers.add_parser('list-users', help="List all users")

    set_user_parser = subparsers.add_parser('set-user', help="Set a user's login and password or create the user if not exist.", )
    set_user_parser.add_argument("login", type=str)

    subparsers.add_parser('list-images', help="List all images")
    update_image_parser = subparsers.add_parser('update-image-status', help="Update the status of an image")
    update_image_parser.add_argument("id", type=int)
    update_image_parser.add_argument("status", type=int)

    args = parser.parse_args()

    if args.sub == "list-users":
        list_users()
    elif args.sub == "set-user":
        set_or_add_user(args.login)
    elif args.sub == "list-images":
        list_images()
    elif args.sub == "update-image-status":
        update_image_status(args.id, args.status)


