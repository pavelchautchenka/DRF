from celery.app import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, User
from django.core.mail import send_mail


@shared_task(routing_key='email.send')
def user_send_notification(subject, message, from_email, recipient_list):
    return send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Event)
def create_event(sender, created, instance: Event, **kwargs):
    if created:
        users_notification = User.objects.filter(notify=True)
        for user in users_notification:
            user_send_notification.delay("Уведомление",
                                         f"Уведомляем вас, что появилось новое событие  {instance.name} \n, "
                                         f"{instance.description} \n,"
                                         f"Мероприятие  проходит в {instance.meeting_time}",
                                         [user.email],
                                         fail_silently=False)
