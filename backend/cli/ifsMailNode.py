#!/usr/bin/python

import traceback
import sys
import urllib
import urllib2


def main():
    try:
        mail_data = sys.stdin.read()

        # you may change this...
        URL = "http://127.0.0.1:5000/mails/"

        post_data_dictionary = {'mail': mail_data}
        post_data_encoded = urllib.urlencode(post_data_dictionary)
        request_object = urllib2.Request(URL, post_data_encoded)
        response = urllib2.urlopen(request_object)

        response_msg = response.read()

        if response.getcode() != 200 or response_msg != "OK!":
            print response_msg
            sys.exit(1)
    except SystemExit:
        sys.exit(1)
    except:
        print "Error :( \nPlease contact the admin."
        print ("An uncaught exception in the cli: \n%s" % traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "--debug":
        from os import path

        print "DEBUG! Faking sys.stdin"
        # mail = "mail_wo_image"
        mail = "mail_very_big"
        ROOT = path.join(path.dirname(__file__), "../../")
        test_file = path.join(ROOT, "test-data/%s" % mail)
        with open(test_file) as fi:
            sys.stdin = fi
            main()
    else:
        main()
