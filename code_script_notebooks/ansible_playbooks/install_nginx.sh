apt update -y
apt install nginx1.12
nginx -v
systemctl start nginx
systemctl enable nginx