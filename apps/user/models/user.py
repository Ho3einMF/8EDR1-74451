from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    class Meta:
        db_table = "user_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
