# Generated by Django 3.0.4 on 2020-03-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_auto_20200326_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.TextField(default=''),
        ),
    ]
