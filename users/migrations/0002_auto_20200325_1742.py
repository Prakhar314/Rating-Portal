# Generated by Django 3.0.4 on 2020-03-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='bannedTill',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
