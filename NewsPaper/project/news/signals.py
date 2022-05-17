from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.title} {instance.text}'
    else:
        subject = f'В посте произошли изменения: {instance.title} {instance.text}'
    mail_managers(
        subject=subject,
        message=instance.text,
    )


@receiver(post_delete, sender=Post)
def notify_managers_appointment_canceled(sender, instance, **kwargs):
    subject = f'{instance.title} - эта новость была удалена!'
    mail_managers(
        subject=subject,
        message=instance.text,
    )
