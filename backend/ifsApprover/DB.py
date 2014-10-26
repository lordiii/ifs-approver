import hashlib
import sqlite3
import time

import Log
from ifsApprover.Utils import rnd_string


logger = Log.get_logger("DB")


class DB():
    STATUS_OK = 1
    STATUS_NO_IMAGE = 2
    STATUS_APPROVED = 3
    STATUS_REJECTED = 4

    _SYSTEM_USER = "_system_".lower()

    def __init__(self, filename):
        self._connection = sqlite3.connect(filename, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()
        if not self._exist_table("users"):
            self._create_table_users()
        if not self._exist_table("images"):
            self._create_table_images()

    def _exist_table(self, table_name):
        self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='%s'" % table_name)
        return self._cursor.fetchone()[0] == 1

    def _create_table_images(self):
        logger.info("Creating tables images")
        self._cursor.execute("""
        CREATE TABLE images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            filename TEXT,
            status INT NOT NULL,
            description TEXT,
            date INT NOT NULL,
            width INT,
            height INT,
            changed_by INTEGER,
            action_reason TEXT,
            FOREIGN KEY(changed_by) REFERENCES users(id)
        )""")

    def _create_table_users(self):
        logger.info("Creating tables users")
        self._cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )""")

        data = (0, DB._SYSTEM_USER, "-", "-")
        self._cursor.execute("""
        INSERT INTO users
            (id, login, password, salt)
            VALUES (?, ?, ?, ?)
        """, data)
        self._connection.commit()

    def is_system_user(self, user):
        return user["login"] == DB._SYSTEM_USER


    #
    # Images
    #

    def _insert_images(self, sender, description, status, filename=None, width=None, height=None, changed_by=None):
        now = int(time.time())
        data = (sender, filename, status, description, now, width, height, changed_by)
        logger.debug("Insert new entry: %s" % str(data))

        self._cursor.execute("""
        INSERT INTO images
            (sender, filename, status, description, date, width, height, changed_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        self._connection.commit()

    def add_image(self, sender, description, filename, width, height):
        self._insert_images(
            sender=sender,
            description=description,
            status=self.STATUS_OK,
            filename=filename,
            width=width,
            height=height
        )

    def add_no_image(self, sender, description):
        self._insert_images(sender, description, self.STATUS_NO_IMAGE)

    def get_pending_images(self):
        self._cursor.execute("SELECT * FROM images where status = ? ORDER BY date", [self.STATUS_OK])
        return self._cursor.fetchall()

    def get_pending_images_count(self):
        self._cursor.execute("SELECT count(*) FROM images where status = ? ORDER BY date", [self.STATUS_OK])
        return self._cursor.fetchone()[0]

    def get_missing_images(self):
        self._cursor.execute("SELECT * FROM images where status = ? ORDER BY date", [self.STATUS_NO_IMAGE])
        return self._cursor.fetchall()

    def get_processed_images(self):
        """
        Gets all images that are APPROVED or REJECTED
        :return:
        """
        self._cursor.execute(
            "SELECT i.*, u.login AS changed_by_name FROM images i, users u where u.id = i.changed_by AND status in(?, ?) ORDER BY date",
            [self.STATUS_REJECTED, self.STATUS_APPROVED])
        return self._cursor.fetchall()

    def _change_image(self, image_id, user_login, status, reason="null"):
        if user_login == DB._SYSTEM_USER:
            user_id = 0
        else:
            user_id = self.get_user_id(user_login)
            if user_id is None:
                raise StandardError("user login should not be None at this time.")

        logger.info("Change the image id %s by user %s to %s (reason %s)" % (image_id, user_login, status, reason))
        self._cursor.execute("UPDATE images SET status = :status, changed_by = :by, action_reason = :reason WHERE id = :imgId",
                             {"status": status, "by": user_id, "reason": reason, "imgId": image_id})
        self._connection.commit()

    def get_single_image(self, image_id):
        self._cursor.execute("SELECT * FROM images where id = ?", [image_id])
        return self._cursor.fetchone()

    def approve_image(self, image_id, user_login):
        self._change_image(image_id, user_login, DB.STATUS_APPROVED)

    def reject_image(self, image_id, user_login, reject_reason):
        self._change_image(image_id, user_login, DB.STATUS_REJECTED, reason=reject_reason)

    def update_image_by_system(self, image_id, status):
        self._change_image(image_id, DB._SYSTEM_USER, status)


    #
    # User
    #

    @staticmethod
    def _hash_password(plain_text, salt):
        return hashlib.sha512(plain_text + salt).hexdigest()

    def get_users_list(self):
        self._cursor.execute("SELECT id, login FROM users")
        return self._cursor.fetchall()

    def check_login(self, login, plain_password):
        login = login.lower()
        self._cursor.execute("SELECT salt FROM users where login = ?", [login])
        salt = self._cursor.fetchone()
        if salt is None:
            return False
        salt = salt[0]

        password = self._hash_password(plain_password, salt)
        self._cursor.execute("SELECT count(id) FROM users where login = ? and password = ?", [login, password])
        return self._cursor.fetchone()[0] == 1

    def add_user(self, login, plain_password):
        login = login.lower()
        logger.info("Creating new user %s", login)
        salt = rnd_string(8)
        password = self._hash_password(plain_password, salt)
        data = (login, password, salt)
        self._cursor.execute("""
        INSERT INTO users
            (login, password, salt)
            VALUES (?, ?, ?)
        """, data)
        self._connection.commit()

    def get_user_id(self, login):
        login = login.lower()
        if login == DB._SYSTEM_USER:
            return None
        self._cursor.execute("SELECT id FROM users where login = ?", [login])
        result = self._cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def update_password(self, login, new_plain_password):
        login = login.lower()
        logger.info("Updating user %s", login)
        salt = rnd_string(8)
        password = self._hash_password(new_plain_password, salt)
        self._cursor.execute("UPDATE users SET salt = ?, password = ? WHERE login = ?", [salt, password, login])
        self._connection.commit()
