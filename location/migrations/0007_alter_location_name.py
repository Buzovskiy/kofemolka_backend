# Generated by Django 4.2.6 on 2024-11-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_alter_locationimage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name in application'),
        ),
    ]
