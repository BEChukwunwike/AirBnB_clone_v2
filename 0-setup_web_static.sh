#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static
apt-get -y update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "AirBnB Clone test" | tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
sed -i '16i\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html index.htm;\n\t}' /etc/nginx/sites-available/default
service nginx start
