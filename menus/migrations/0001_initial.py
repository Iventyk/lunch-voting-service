# Generated manually for the lunch voting service.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("restaurants", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("items", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menus",
                        to="restaurants.restaurant",
                    ),
                ),
            ],
            options={"ordering": ["-date", "restaurant__name"]},
        ),
        migrations.AddConstraint(
            model_name="menu",
            constraint=models.UniqueConstraint(fields=("restaurant", "date"), name="unique_daily_menu_per_restaurant"),
        ),
    ]
