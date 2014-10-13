from os import path, makedirs
import uuid


def make_dirs_if_needed(filename):
    dir = path.dirname(filename)
    if not path.exists(dir):
        makedirs(dir)


def rnd_string(char_count):
    return str(uuid.uuid4().get_hex().upper()[0:char_count])