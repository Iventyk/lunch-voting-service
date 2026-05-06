import pytest
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import create_user

pytestmark = pytest.mark.django_db


def test_user_can_obtain_jwt_token():
    create_user(username="john", password="strong-password")
    response = APIClient().post(
        "/api/auth/token/",
        {"username": "john", "password": "strong-password"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


def test_employee_creation_requires_admin_user():
    client = APIClient()
    client.force_authenticate(create_user())

    response = client.post(
        "/api/employees/",
        {
            "username": "new",
            "password": "password123",
            "full_name": "New Employee",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
