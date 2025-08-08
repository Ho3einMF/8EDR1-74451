from rest_framework import generics, permissions

from apps.reserve.models import Reservation
from apps.reserve.serializers import ReserveSerializer


class ReserveAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReserveSerializer


class CancelReserveAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "reservation_id"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        table = instance.table
        table.is_reserved = False
        table.save()

        super().perform_destroy(instance)
