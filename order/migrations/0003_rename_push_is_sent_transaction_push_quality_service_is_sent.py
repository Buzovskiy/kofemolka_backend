# Generated by Django 4.2.6 on 2024-02-18 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_transaction_push_is_sent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='push_is_sent',
            new_name='push_quality_service_is_sent',
        ),
    ]
