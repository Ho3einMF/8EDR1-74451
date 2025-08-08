from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.reserve.models import Table
from apps.user.models import User


class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("user"),
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("table"),
    )
    individuals = models.PositiveIntegerField(_("individuals"))
    cost = models.DecimalField(_("cost"), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    class Meta:
        db_table = "reserve_reservation"
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")

    def __str__(self):
        return f"Reservation {self.id} for {self.user} in table {self.table}"
