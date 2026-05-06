from datetime import date

from django.db import transaction

from menus.models import Menu
from restaurants.models import Restaurant


@transaction.atomic
def upsert_menu(*, restaurant: Restaurant, menu_date: date, items: list[dict]) -> Menu:
    """Create or replace a restaurant menu for the given day."""
    menu, _created = Menu.objects.update_or_create(
        restaurant=restaurant,
        date=menu_date,
        defaults={"items": items},
    )
    return menu
