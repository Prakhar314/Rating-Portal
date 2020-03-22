# Generated by Django 3.0.4 on 2020-03-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('score', models.DecimalField(decimal_places=2, max_digits=2)),
                ('reviewContent', models.TextField()),
                ('courseName', models.CharField(max_length=120)),
            ],
        ),
    ]
