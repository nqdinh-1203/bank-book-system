# Generated by Django 4.0.3 on 2022-03-18 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_tag_orders_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='tags',
        ),
        migrations.AddField(
            model_name='products',
            name='tags',
            field=models.ManyToManyField(to='account.tag'),
        ),
    ]
