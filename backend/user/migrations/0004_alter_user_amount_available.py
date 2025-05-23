# Generated by Django 4.2.18 on 2025-03-24 21:35

from decimal import Decimal

import django.core.validators
import djmoney.models.fields
import djmoney.money
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='amount_available',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', max_digits=10, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0.0, 'USD'))]),
        ),
    ]
