#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate

# 🔥 FORCE create/update superuser
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(username='admin')
user.set_password('admin123')
user.is_superuser = True
user.is_staff = True
user.save()
" | python manage.py shell

python manage.py collectstatic --noinput