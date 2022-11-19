# Generated by Django 4.1.3 on 2022-11-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_remove_like_accepter_remove_like_liked_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="content",
            new_name="comment",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="replies",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="reply_to",
        ),
        migrations.AlterField(
            model_name="comment",
            name="author",
            field=models.JSONField(default=dict),
        ),
    ]