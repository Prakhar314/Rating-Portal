# Generated by Django 3.0.4 on 2020-03-24 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reviewReported',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='review.Review'),
        ),
    ]