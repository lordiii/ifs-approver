#!/usr/bin/python3

import sys
from ifsApprover.web import app

sys.path.append("../")

# run standalone for debugging
if __name__ == "__main__":
    app.run(debug=False)