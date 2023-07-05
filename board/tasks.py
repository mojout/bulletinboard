import os

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Announcement


@shared_task
def ann_created(announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    subject = f'Новое объявление: {announcement.title}'
    message = f'Уважаемый пользователь,\n\n' \
              f'у нас появилось новое объявление в категории {announcement.category},\n\n' \
              f'Спешите быть первым!'
    mail_sent = send_mail(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), [User.email])
    return mail_sent
