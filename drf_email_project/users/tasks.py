from __future__ import absolute_import, unicode_literals

from rest_framework.response import Response
from celery import shared_task
from django.core.mail import EmailMessage
from time import sleep


@shared_task()
def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'],
        to=(data['to_email'],))
    email.send()
