from django.conf import settings
from django.db import models

from menus.models import Menu


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="votes"
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique_user_vote_per_day"
            )
        ]
        ordering = ["-date", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.user} voted for {self.menu}"
