# Generated by Django 5.1.1 on 2024-11-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_balance_remove_items_balance_alter_items_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='remaining_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='balance',
            name='spend_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
