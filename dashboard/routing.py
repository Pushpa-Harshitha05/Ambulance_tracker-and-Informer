from django.urls import re_path
from dashboard.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/notify/(?P<hospital_id>\w+)/$', NotificationConsumer.as_asgi()),
]