# Generated by Django 4.2.6 on 2024-11-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0008_merge_20241111_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='spot_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Location name (Poster)'),
        ),
    ]