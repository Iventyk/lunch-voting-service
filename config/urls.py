from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from menus.views import MenuViewSet
from restaurants.views import RestaurantViewSet
from users.views import EmployeeViewSet
from votes.views import VoteViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("menus", MenuViewSet, basename="menu")
router.register("votes", VoteViewSet, basename="vote")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/", include(router.urls)),
]
