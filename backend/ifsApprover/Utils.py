from os import path, makedirs
import subprocess
import uuid


def make_dirs_if_needed(filename):
    dir = path.dirname(filename)
    if not path.exists(dir):
        makedirs(dir)


def rnd_string(char_count):
    return str(uuid.uuid4().get_hex().upper()[0:char_count])


def run(command, name_for_error):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.read().rstrip()
    return_code = p.wait()
    if return_code != 0:
        raise StandardError("%s failed. Log: \n%s" % (name_for_error, out))

    return out