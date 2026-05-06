from datetime import date

from django.db.models import QuerySet
from django.utils import timezone

from menus.models import Menu


def menus_for_date(menu_date: date | None = None) -> QuerySet[Menu]:
    target_date = menu_date or timezone.localdate()
    return Menu.objects.select_related("restaurant").filter(
        date=target_date,
        restaurant__is_active=True,
    )
