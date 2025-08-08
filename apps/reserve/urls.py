from django.urls import path

from apps.reserve import apis


urlpatterns = [
    path("", apis.ReserveAPIView.as_view(), name="reserve-api"),
    path(
        "<int:reservation_id>/cancel/",
        apis.CancelReserveAPIView.as_view(),
        name="cancel-reserve-api",
    ),
]
