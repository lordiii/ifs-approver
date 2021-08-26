# ifs-approver

The workflow for this tool:

1.  Someone makes a nice image for the "image from space" category
2.  Mails the image to a special address
3.  Parse the email and sends a notification to reviewer
4.  The reviewer approves or disapproves the image

# Setup

Our setup, your setup may vary.

## mail

Receive emails and run a python script. 

    # /etc/postfix/master.cf
    ifs unix - n n - - pipe
         flags=F user=ifs argv=/path/to/script/ifsMailNode.py


    # /etc/postfix/virtual_alias
    # used as 'virtual_alias_maps' in main.cf
    mail_address_to_trigger@your_server            ifs
    
Don't forget to change the ```url``` value in the url ```/path/to/script/ifsMailNode.py``` script.

## app

```shell
apt-get install nginx python3-venv python3-pip python3-wheel uwsgi uwsgi-plugin-python3 imagemagick
```

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
    
The config    
```ini
[uwsgi]
plugin          = python3
virtualenv      = /home/album/ifs-approver/backend/venv
pythonpath      = /home/album/ifs-approver/backend/venv

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
chown-socket = www-data:www-data
chmod-socket = 664
```

Make/prepare the app

```shell
git clone https://github.com/ktt-ol/ifs-approver.git
cd ifs-approver

# make frontend
cd frontend
npm ci
npm run build

# make the backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup the configurations

    cp config.example.py config.py
    vim config.py
    
# TODO

* More mails
    * User error mail
* Cleanup for broken/missing images
