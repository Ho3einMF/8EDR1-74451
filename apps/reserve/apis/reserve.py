from rest_framework import generics, permissions

from apps.reserve.serializers import ReserveSerializer


class ReserveAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReserveSerializer
