from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class AvailableTableNotFound(exceptions.NotFound):
    default_detail = _("available table not found.")
