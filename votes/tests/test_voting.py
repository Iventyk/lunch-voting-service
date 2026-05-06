import pytest
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import create_menu, create_user
from votes.models import Vote

pytestmark = pytest.mark.django_db


def test_api_v2_user_can_change_daily_vote():
    user = create_user()
    first_menu = create_menu("First")
    second_menu = create_menu("Second")
    client = APIClient()
    client.force_authenticate(user)

    first_response = client.post(
        "/api/votes/",
        {"menu_id": first_menu.id},
        format="json",
        HTTP_X_API_VERSION="2",
    )
    second_response = client.post(
        "/api/votes/",
        {"menu_id": second_menu.id},
        format="json",
        HTTP_X_API_VERSION="2",
    )

    assert first_response.status_code == status.HTTP_201_CREATED
    assert second_response.status_code == status.HTTP_200_OK
    assert Vote.objects.get(user=user).menu == second_menu


def test_api_v1_user_cannot_change_daily_vote():
    user = create_user()
    first_menu = create_menu("First")
    second_menu = create_menu("Second")
    client = APIClient()
    client.force_authenticate(user)

    client.post(
        "/api/votes/",
        {"menu_id": first_menu.id},
        format="json",
        HTTP_X_API_VERSION="1",
    )
    response = client.post(
        "/api/votes/",
        {"menu_id": second_menu.id},
        format="json",
        HTTP_X_API_VERSION="1",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Vote.objects.get(user=user).menu == first_menu


def test_results_return_current_day_vote_counts():
    user = create_user()
    menu = create_menu("Winner")
    Vote.objects.create(user=user, menu=menu, date=menu.date)
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/votes/results/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["votes_count"] == 1
