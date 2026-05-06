from rest_framework import serializers

from common.versioning import get_api_version
from menus.models import Menu
from menus.serializers import MenuSerializer
from votes.models import Vote
from votes.services import cast_vote


class VoteCreateSerializer(serializers.Serializer):
    menu_id = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.select_related("restaurant"),
        source="menu",
    )

    def create(self, validated_data):
        request = self.context["request"]
        result = cast_vote(
            user=request.user,
            menu=validated_data["menu"],
            api_version=get_api_version(request),
        )
        self.context["vote_created"] = result.created
        return result.vote


class VoteSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "menu", "date", "created_at", "updated_at"]


class ResultSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name", read_only=True
    )
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "date",
            "items",
            "votes_count",
        ]
