from django.contrib.auth import get_user_model
from django.utils import timezone

from menus.models import Menu
from restaurants.models import Restaurant

User = get_user_model()


def create_user(
    username: str = "employee",
    password: str = "password123",
    *,
    is_staff: bool = False,
):
    return User.objects.create_user(
        username=username, password=password, is_staff=is_staff
    )


def create_menu(
    name: str = "Cafe", *, items: list[dict] | None = None, date=None
) -> Menu:
    restaurant = Restaurant.objects.create(name=name)
    return Menu.objects.create(
        restaurant=restaurant,
        date=date or timezone.localdate(),
        items=items or [{"name": "Soup", "price": "5.00"}],
    )
