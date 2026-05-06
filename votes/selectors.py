from datetime import date

from django.db.models import Count, QuerySet
from django.utils import timezone

from menus.models import Menu


def current_day_results(menu_date: date | None = None) -> QuerySet[Menu]:
    target_date = menu_date or timezone.localdate()
    return (
        Menu.objects.select_related("restaurant")
        .filter(date=target_date, restaurant__is_active=True)
        .annotate(votes_count=Count("votes"))
        .order_by("-votes_count", "restaurant__name")
    )
