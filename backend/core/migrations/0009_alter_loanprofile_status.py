# Generated by Django 3.2.25 on 2024-09-24 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_loanprofile_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanprofile',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Rejected')], default=1, help_text='The status of the loan profile.'),
        ),
    ]
