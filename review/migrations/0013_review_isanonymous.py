# Generated by Django 3.0.4 on 2020-03-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0012_dislike_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='isAnonymous',
            field=models.BooleanField(default=False),
        ),
    ]