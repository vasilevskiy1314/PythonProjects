import logging

import requests
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from ...models import *
from datetime import datetime, timedelta
from django.shortcuts import reverse
from django.utils import timezone


logger = logging.getLogger(__name__)


def my_job():
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
    print('gg')


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/2"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")