from django.contrib import admin
from django.urls import path
from .views import (EventViewSet, UserListView, RegisterUserView, SignupEventView,
                    EventsMyViewSet)

app_name = 'Event:api'
urlpatterns = [

    path('events/', EventViewSet.as_view(), name='event_list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/register', RegisterUserView.as_view(), name='register-user'),
    path('event/<int:id>/', SignupEventView.as_view(), name='signup-event'),
    path('events/my/', EventsMyViewSet.as_view(), name='events')
]
