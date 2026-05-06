from django.utils import timezone
from rest_framework import serializers

from menus.models import Menu
from menus.services import upsert_menu
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.filter(is_active=True),
        source="restaurant",
        write_only=True,
    )

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "restaurant_id", "date", "items", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_items(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError("Menu items must be a non-empty list.")
        return value

    def create(self, validated_data):
        return upsert_menu(
            restaurant=validated_data["restaurant"],
            menu_date=validated_data.get("date") or timezone.localdate(),
            items=validated_data["items"],
        )
