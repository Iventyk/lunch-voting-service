from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from menus.models import Menu
from votes.models import Vote


@dataclass(frozen=True)
class VoteResult:
    vote: Vote
    created: bool


@transaction.atomic
def cast_vote(*, user, menu: Menu, api_version: int) -> VoteResult:
    today = timezone.localdate()
    if menu.date != today:
        raise serializers.ValidationError(
            {"menu_id": "Voting is allowed only for today's menus."}
        )

    existing_vote = (
        Vote.objects.select_for_update().filter(user=user, date=today).first()
    )
    if existing_vote is None:
        return VoteResult(
            Vote.objects.create(user=user, menu=menu, date=today), True
        )

    if api_version == 1:
        raise serializers.ValidationError(
            "API version 1 allows only one immutable vote per day."
        )

    existing_vote.menu = menu
    existing_vote.save(update_fields=["menu", "updated_at"])
    return VoteResult(existing_vote, False)
