# Generated by Django 3.1.6 on 2022-10-21 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('source', models.CharField(blank=True, max_length=500)),
                ('origin', models.CharField(blank=True, max_length=500)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('unlisted', models.BooleanField(default=False)),
                ('contentType', models.TextField(max_length=2000)),
                ('visibility', models.TextField(max_length=2000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]