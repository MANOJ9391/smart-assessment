#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate

# 🔥 create superuser automatically
echo "from django.contrib.auth.models import User; 
User.objects.filter(username='admin').exists() or 
User.objects.create_superuser('admin','admin@gmail.com','admin123')" | python manage.py shell

python manage.py collectstatic --noinput