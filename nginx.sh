#!/bin/bash

sudo cp -rf wanebu-backend-login.conf /etc/nginx/sites-available/login_ms
chmod 777 /var/lib/jenkins/workspace/wanebu-backend-login-cicd

sudo ln -sf /etc/nginx/sites-available/login_ms /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "nginx has been started"

sudo systemctl status nginx