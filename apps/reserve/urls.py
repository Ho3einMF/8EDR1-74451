from django.urls import path

from apps.reserve import apis


urlpatterns = [
    path("", apis.ReserveAPIView.as_view(), name="reserve-api"),
]
