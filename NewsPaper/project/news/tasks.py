from celery import shared_task
import time
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, Post
from datetime import datetime, timedelta
from django.core.mail import send_mail


@shared_task
def new_post_sub_email(sub_categoryname):
    post_bject = Post.objects.all().order_by("-id")[0]
    post_category = Category.objects.get(pk=sub_categoryname)
    for user in User.objects.filter(category=sub_categoryname):
        # получаем наш html
        html_content = render_to_string(
            'subs_email.html',
            {
                'sub_email_text': post_object.text,
                'sub_email_title': post_object.title,
                'sub_username': user.username,
                'sub_categoryname': post_category.name
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Вышла новаяCELERY статья {post_object.title} в вашей любимой категории {post_category.name}',
            body=f'{user.username}, {post_object.text}',
            from_email='vapython@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def list_of_week_posts():
    date = datetime.now() - timedelta(days=7)
    message = ''
    i = 1
    for user in User.objects.filter(category=Category.objects.get(pk=i)):
        i += 1
        for week_new in Post.objects.filter(dateCreation__range=[date, datetime.now()]):
            message += f'http://127.0.0.1:8000{week_new.get_absolute_url()}, '
        send_mail(
            'News in the week!',
            f'За прошлую неделю вышли новости: {message}',
            from_email='vasilevskiyak@yandex.ru',
            recipient_list=[user.email],
        )
