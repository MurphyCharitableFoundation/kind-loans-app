# Generated by Django 4.2.18 on 2025-03-25 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0007_loanprofile_city_loanprofile_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
