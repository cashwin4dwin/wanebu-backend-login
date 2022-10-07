#!/bin/bash

sudo cp -rf wanebu-backend-login.conf /etc/nginx/sites-available/wanebu-backend-login
chmod 710 /var/lib/jenkins/workspace/wanebu-backend-new-cicd

sudo ln -sf /etc/nginx/sites-available/wanebu-backend-login /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "nginx has been started"

sudo systemctl status nginx