# Generated by Django 4.0.3 on 2022-05-25 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_bankbookk_bankbook'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankBookkk',
            fields=[
                ('customer_name', models.CharField(max_length=200, null=True, verbose_name='Tên khách hàng')),
                ('identityid', models.CharField(max_length=200, null=True, verbose_name='CMND/CCCD')),
                ('customer_address', models.CharField(max_length=200, null=True, verbose_name='Địa chỉ')),
                ('bookid', models.AutoField(primary_key=True, serialize=False)),
                ('firstdeposit', models.FloatField(null=True, verbose_name='Số tiền gửi')),
                ('balance', models.FloatField(default=0, null=True)),
                ('type', models.CharField(choices=[('3 tháng', '3 tháng'), ('6 tháng', '6 tháng'), ('Không kỳ hạn', 'Không kỳ hạn')], max_length=200, null=True, verbose_name='Loại tiết kiệm')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customer')),
            ],
        ),
    ]