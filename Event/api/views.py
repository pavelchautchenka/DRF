from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from Event.cache import get_cached
from Event.models import Event, User
from .serializers import EventSerializer, UserSerializer


class EventsMyViewSet(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)


class SignupEventView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request, id):
        event = get_object_or_404(Event, pk=id, meeting_time__gt=timezone.now())
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def post(self, request, id, **kwargs, ):
        event = get_object_or_404(Event, pk=id, meeting_time__gt=timezone.now())
        event.users.add(request.user)
        return Response({"message": "Successfully subscribed to the event"})


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer()
        return Response({'serializer': serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class EventViewSet(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Event.objects.filter(meeting_time__gt=timezone.now())
        return get_cached("events", queryset, 300)
