# Generated by Django 3.0.4 on 2020-03-24 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20200324_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reviewReported',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='review.Review'),
        ),
    ]