# Generated by Django 4.2.6 on 2023-10-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setting',
            options={'verbose_name': 'Settings', 'verbose_name_plural': 'Settings'},
        ),
        migrations.AddField(
            model_name='setting',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
