from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker

from apps.user.models import User
from apps.reserve.models import Table, Reservation


class CancelBookAPITestCase(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.other_user = baker.make(User)
        self.client.force_authenticate(user=self.user)

    def _get_cancel_url(self, reservation_id):
        return reverse("cancel-reserve-api", args=[reservation_id])

    def test_cancel_reservation_success(self):
        table = baker.make(Table, capacity=4, is_reserved=True)
        reservation = baker.make(Reservation, user=self.user, table=table)
        url = self._get_cancel_url(reservation.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
        table.refresh_from_db()
        self.assertFalse(table.is_reserved)

    def test_cancel_reservation_unauthenticated_fail(self):
        table = baker.make(Table, capacity=4, is_reserved=True)
        reservation = baker.make(Reservation, user=self.user, table=table)
        self.client.logout()
        url = self._get_cancel_url(reservation.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancel_reservation_not_found_fail(self):
        url = self._get_cancel_url(999)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_cancel_another_users_reservation(self):
        table = baker.make(Table, capacity=4, is_reserved=True)
        reservation = baker.make(Reservation, user=self.other_user, table=table)
        url = self._get_cancel_url(reservation.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Reservation.objects.filter(id=reservation.id).exists())
        table.refresh_from_db()
        self.assertTrue(table.is_reserved)
