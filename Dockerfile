FROM debian:10.10-slim

RUN set -ex && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    # needed for the app
    nginx python3-venv python3-pip python3-wheel uwsgi uwsgi-plugin-python3 imagemagick \
    # needed for docker environment
    supervisor && \
  useradd ifs && \
  mkdir /ifs-backend && \
  chown ifs:ifs /ifs-backend

RUN set -ex && \
    rm /etc/nginx/sites-enabled/default && \
    bash -c "echo 'daemon off;' >> /etc/nginx/nginx.conf" && \
    # logs nginx errors to console
    rm /var/log/nginx/error.log && ln -s /dev/stderr /var/log/nginx/error.log
ADD docker-support/ifs.nginx /etc/nginx/sites-enabled/
ADD docker-support/ifs.uwsgi /etc/uwsgi/apps-enabled/ifs.ini

ADD docker-support/supervisord.conf /etc/

ADD backend/requirements.txt /ifs-backend/
RUN set -ex && \
  cd /ifs-backend && \
  python3 -m venv venv && \
  . venv/bin/activate && \
  pip install wheel && \
  pip install -r requirements.txt

CMD ["/usr/bin/supervisord"]