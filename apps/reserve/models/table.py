from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Table(models.Model):
    number = models.PositiveIntegerField(_("table number"), unique=True)
    capacity = models.IntegerField(
        _("capacity"), validators=[MinValueValidator(4), MaxValueValidator(10)]
    )
    is_reserved = models.BooleanField(_("is reserved"), default=False)

    class Meta:
        db_table = "reserve_table"
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")

    def __str__(self):
        return f"Table {self.id} (Seats: {self.capacity})"
