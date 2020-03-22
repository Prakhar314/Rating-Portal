# Generated by Django 3.0.4 on 2020-03-22 13:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-dateAdded']},
        ),
        migrations.AddField(
            model_name='review',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]