# ifs-approver

The workfow for this tool:

1.  Someone makes a nice image for the "image from space" category
1.  Mails the image to a special address
1.  Parse the email and sends a notification to reviewer
1.  The reviewer approves or disapproves the image

# Setup

## Server setup

Our setup, your setup may vary.
 
Receive emails and run a python script. 

    # /etc/postfix/master.cf
    ifs unix - n n - - pipe
         flags=F user=ifs argv=/path/to/script/ifsMailNode.py


    # /etc/postfix/virtual_alias
    # used as 'virtual_alias_maps' in main.cf
    mail_address_to_trigger@your_server            ifs
    
Don't forget to change the ```url``` value in the url ```/path/to/script/ifsMailNode.py``` script.


Setup the server running the python backend (and the JS frontend). We use a nginx backend.

    # /etc/nginx/sites-enabled/ifs
    server {
        listen 80;
        listen [::]:80;
    
        server_name your_server_name;
        client_max_body_size    20M;
        location / {
            gzip off;
            include uwsgi_params;
            uwsgi_param SCRIPT_NAME /;
            uwsgi_modifier1 30;
            uwsgi_pass unix:/run/uwsgi/app/ifs/socket;
        }
    }

nginx uses uwsgi to serve the python backend. We use 'album' as user. 
    
    apt-get install uwsgi-plugin-python
    
The config    
    
    # /etc/uwsgi/apps-enabled
    [uwsgi]
    plugin          = python
    no-site         = True
    pythonpath      = /usr/lib/python2.7/dist-packages
    pythonpath      = /usr/local/lib/python2.7/dist-packages
    chdir           = /home/album/ifs-approver/backend
    wsgi-file       = /home/album/ifs-approver/backend/cgi/ifs-approver.wsgi.py
    
    uid = album
    gid = album
    
    callable = app
    
    # process-related settings
    # master
    master          = true
    # maximum number of worker processes
    processes       = 2
    # the socket (use the full path to be safe
    socket = /run/uwsgi/app/ifs/socket

Reload
    
    service nginx reload
    service uwsgi reload
    
## Programm setup

Install requirements
    
    apt-get install python-pip python-imaging
    apt-get install node-js
    # todo.... install npm, bower

Make/prepare the app

    git clone https://github.com/ktt-ol/ifs-approver.git
    cd ifs-approver
    
    # make frontend
    cd frontend
    npm install
    bower install
    grunt build

    # make the backend
    cd ../backend
    pip install -r requirements.txt

Setup the configurations

    cp config.example.py config.py
    vim config.py
    
# TODO

* More mails
    * User error mail
* Check responsive for 1280 width
* Cleanup for broken/missing images

