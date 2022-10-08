#!/bin/bash

source wlenv/bin/activate

cd /var/lib/jenkins/workspace/wanebu-backend-login-cicd/login_ms

python3 manage.py makemigrations
python3 manage.py migrate

echo "Migrations done"

cd /var/lib/jenkins/workspace/wanebu-backend-login-cicd

sudo -i

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"



sudo systemctl daemon-reload
sudo systemctl start gunicorn

echo "Gunicorn has started."

sudo systemctl enable gunicorn

echo "Gunicorn has been enabled."

sudo systemctl restart gunicorn


sudo systemctl status gunicorn

