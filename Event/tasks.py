from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event


@shared_task(ignore_result=True, routing_key='email.send')
def send_event_reminders():
    current_time = timezone.now()
    one_day = current_time + timedelta(days=1)
    six_hours = current_time + timedelta(hours=6)

    events_one_day = Event.objects.filter(meeting_time__range=(current_time, one_day))
    events_six_hours = Event.objects.filter(meeting_time__range=(current_time, six_hours))

    for event in events_one_day:
        for user in event.users.all():
            send_mail("Уведомление", f"Уведомляем вас, что вы согласились посетить {event.name} \n, {event.description} \n,"
                      f"Мероприятие  проходит завтра  в {event.meeting_time}", "litivin1987@yandex.ru",[user.email],)

    for event in events_six_hours:
        for user in event.users.all():
            send_mail("Уведомление", f"Уведомляем вас, что вы согласились посетить {event.name} \n, {event.description} \n,"
                      f"Мероприятие  проходит сегодня  в {event.meeting_time}","litivin1987@yandex.ru", [user.email], )

