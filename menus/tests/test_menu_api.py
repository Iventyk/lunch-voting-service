import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import create_user
from menus.models import Menu
from restaurants.models import Restaurant

pytestmark = pytest.mark.django_db


def test_admin_can_upload_daily_menu():
    admin = create_user(username="admin", is_staff=True)
    restaurant = Restaurant.objects.create(name="Pasta House")
    client = APIClient()
    client.force_authenticate(admin)

    response = client.post(
        "/api/menus/",
        {
            "restaurant_id": restaurant.id,
            "date": timezone.localdate().isoformat(),
            "items": [{"name": "Pasta", "price": "12.00"}],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Menu.objects.filter(
        restaurant=restaurant, date=timezone.localdate()
    ).exists()


def test_authenticated_user_can_get_today_menus():
    user = create_user()
    restaurant = Restaurant.objects.create(name="Sushi Bar")
    Menu.objects.create(
        restaurant=restaurant,
        date=timezone.localdate(),
        items=[{"name": "Roll", "price": "9.00"}],
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/menus/today/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
