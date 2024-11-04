# Generated by Django 3.2.25 on 2024-11-04 04:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('payer_object_id', models.PositiveIntegerField()),
                ('recipient_object_id', models.PositiveIntegerField()),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, help_text='The amount for the transaction.', max_digits=10)),
                ('payment_method', models.IntegerField(choices=[(1, 'Credit Card'), (2, 'Debit Card'), (3, 'PayPal'), (4, 'Apple Pay'), (5, 'Google Pay'), (6, 'Bank Transfer'), (7, 'Cash'), (9, 'Cryptocurrency')], default=3, help_text='The method of payment for the transaction.')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Completed'), (3, 'Failed'), (4, 'Refunded'), (5, 'Canceled'), (6, 'On Hold'), (7, 'Chargeback')], default=1, help_text='The status of the transaction.')),
                ('payer_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_transactions', to='contenttypes.contenttype')),
                ('recipient_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_transactions', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created'],
            },
        ),
    ]
