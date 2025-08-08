from django.db.models import Q, F
from django.db.models.functions import Mod
from django.db import transaction
from rest_framework import serializers

from restaurant_reservation_system.settings import SEAT_COST
from apps.reserve.exceptions import AvailableTableNotFound
from apps.reserve.models import Table, Reservation


class ReserveSerializer(serializers.ModelSerializer):
    number_of_seats = serializers.IntegerField(source="table.capacity", read_only=True)

    class Meta:
        model = Reservation
        fields = ("cost", "table_id", "number_of_seats", "individuals")
        read_only_fields = ("table_id", "cost")
        extra_kwargs = {"individuals": {"write_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        table = self._find_cheapest_table(validated_data["individuals"])

        if not table:
            raise AvailableTableNotFound()

        cost = self._calculate_cost(table.capacity)

        reservation_obj, created = Reservation.objects.get_or_create(
            user=self.context["request"].user,
            table=table,
            defaults={
                "individuals": validated_data["individuals"],
                "cost": cost,
            },
        )

        if created:
            table.is_reserved = True
            table.save()

        return reservation_obj

    @staticmethod
    def _calculate_cost(table_capacity):
        # Booking an entire table costs (M - 1) * X
        return (table_capacity - 1) * SEAT_COST

    @classmethod
    def _find_cheapest_table(cls, individuals):
        queryset = Table.objects.order_by("capacity").filter(is_reserved=False)

        if individuals % 2 == 0:
            # For even individuals, find the first any ("even" or "odd") table order by capacity
            queryset = queryset.filter(capacity__gte=individuals)

        else:
            # For odd individual, first try to find exact capacity
            # then if needed try to find next "even" table order by capacity
            book_full_table_q = Q(capacity=individuals)
            next_even_table_q = Q(capacity__gt=individuals, capacity_remainder=0)

            queryset = queryset.annotate(
                capacity_remainder=Mod(F("capacity"), 2)
            ).filter(book_full_table_q | next_even_table_q)

        table_to_reserve = queryset.first()
        return table_to_reserve
