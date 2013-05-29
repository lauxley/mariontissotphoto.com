#!/bin/sh

cd /home/revolunet/django/mariontissotphoto

chown -R www-data:www-data static/photo
chmod -R 775 static/photo
chown -R www-data:www-data static/thumbnails
chmod -R 775 static/thumbnails
