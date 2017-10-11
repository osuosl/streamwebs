#!/usr/bin/env python

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.http import HttpRequest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm


def find_users_and_send_email():
    users = User.objects.filter(is_active=True)
    for user in users:
        try:

            if user.email:
                print("Sending email for to this email:", user.email)
                form = PasswordResetForm({'email': user.email})

                assert form.is_valid()
                request = HttpRequest()
                request.META['SERVER_NAME'] = 'localhost'
                request.META['SERVER_PORT'] = '8000'
                form.save(
                    request=request,
                    from_email="StreamWebs <noreply@streamwebs.org>",
                    email_template_name=(
                        'registration/initial_password_reset_email.html'))

        except Exception as e:
            print("Error: ", e)
            continue

    print('done')

find_users_and_send_email()
