# Generated by Django 5.0.4 on 2025-01-02 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_remove_post_name_post_category_post_slug_post_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="username",
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]