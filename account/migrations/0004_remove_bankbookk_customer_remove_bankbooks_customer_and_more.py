# Generated by Django 4.0.3 on 2022-05-25 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_bankbookkk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankbookk',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='bankbooks',
            name='customer',
        ),
        migrations.DeleteModel(
            name='BankBook',
        ),
        migrations.DeleteModel(
            name='BankBookk',
        ),
        migrations.DeleteModel(
            name='BankBooks',
        ),
    ]
