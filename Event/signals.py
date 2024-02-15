from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, User
from django.core.mail import send_mail


@receiver(post_save, sender=Event)
def create_event(sender, event, created, **kwargs):
    if created:
        user_send_notification = User.objects.filter(notify=True)
        for user in user_send_notification:
            send_mail("Уведомление",
                      f"Уведомляем вас, что появилось новое событие  {event.name} \n, {event.description} \n,"
                      f"Мероприятие  проходит в {event.meeting_time}", [user.email], fail_silently=False)
