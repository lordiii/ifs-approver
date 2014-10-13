#!/usr/bin/python

import sys
from ifsApprover.Log import init_wsgi_logger
from ifsApprover.web import app

sys.path.append("../")

init_wsgi_logger()

# run standalone for debugging
if __name__ == "__main__":
    app.run(debug=True)