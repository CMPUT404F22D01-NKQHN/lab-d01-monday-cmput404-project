# Generated by Django 4.1.3 on 2022-11-19 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Node",
            fields=[
                ("api_url", models.URLField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                (
                    "proxy_users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="proxy_users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_account",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
