from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker

from apps.user.models import User
from apps.reserve.models import Table, Reservation
from restaurant_reservation_system.settings import SEAT_COST


class BookTableAPITestCase(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client.force_authenticate(user=self.user)
        self.book_table_url = reverse("reserve-api")

    def test_book_table_response_keys(self):
        baker.make(Table, capacity=4, is_reserved=False)
        data = {"individuals": 4}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_keys = {"cost", "table_id", "number_of_seats"}
        self.assertEqual(set(response.data.keys()), expected_keys)

    def test_book_table_unauthenticated_user_fail(self):
        self.client.logout()
        response = self.client.post(self.book_table_url, data={"individuals": 4})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_table_success(self):
        baker.make(Table, capacity=4, is_reserved=False)
        data = {"individuals": 4}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Reservation.objects.filter(user=self.user, individuals=4).exists()
        )
        self.assertTrue(Table.objects.get(capacity=4).is_reserved)
        expected_cost = (4 - 1) * SEAT_COST
        self.assertEqual(response.data["cost"], f"{expected_cost:.2f}")

    def test_book_table_no_available_table_fail(self):
        baker.make(Table, capacity=4, is_reserved=True)
        data = {"individuals": 5}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_table_even_individuals(self):
        baker.make(Table, capacity=6, is_reserved=False)
        baker.make(Table, capacity=8, is_reserved=False)
        data = {"individuals": 6}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["number_of_seats"], 6)

    def test_book_table_odd_individuals_exact_match(self):
        baker.make(Table, capacity=5, is_reserved=False)
        baker.make(Table, capacity=6, is_reserved=False)
        data = {"individuals": 5}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["number_of_seats"], 5)

    def test_book_table_odd_individuals_finds_next_even(self):
        baker.make(Table, capacity=6, is_reserved=False)
        baker.make(Table, capacity=7, is_reserved=False)
        data = {"individuals": 5}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["number_of_seats"], 6)

    def test_book_table_finds_cheapest_option(self):
        baker.make(Table, capacity=8, is_reserved=False)
        baker.make(Table, capacity=6, is_reserved=False)
        data = {"individuals": 6}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["number_of_seats"], 6)

    def test_book_table_already_reserved_returns_not_found(self):
        table = baker.make(Table, capacity=4, is_reserved=True)
        baker.make(Reservation, user=self.user, table=table, individuals=4)
        data = {"individuals": 4}
        response = self.client.post(self.book_table_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Reservation.objects.filter(user=self.user).count(), 1)
