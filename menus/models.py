from django.db import models

from restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menus",
    )
    date = models.DateField()
    items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "date"],
                name="unique_daily_menu_per_restaurant",
            )
        ]
        ordering = ["-date", "restaurant__name"]

    def __str__(self) -> str:
        return f"{self.restaurant.name} menu for {self.date}"
