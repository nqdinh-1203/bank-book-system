# Generated by Django 4.0.3 on 2022-05-26 06:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankBookkkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Tên loại tiết kiệm')),
                ('minimum_deposit_amount', models.DecimalField(decimal_places=2, default=100000, max_digits=12, verbose_name='Số tiền gửi tối thiểu')),
                ('minimum_withdrawal_amount', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Sẽ được hiệu chỉnh sau', max_digits=12, null=True)),
                ('maximum_withdrawal_amount', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Sẽ được hiệu chỉnh sau', max_digits=12, null=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, help_text='Tỷ lệ từ 0 - 100%', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Tỷ lệ lãi suất')),
                ('period', models.PositiveSmallIntegerField(help_text='Độ dài là 0 tương ứng với Không kỳ hạn', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)], verbose_name='Độ dài kỳ hạn ')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='logo2.png', null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200, null=True, verbose_name='Tên khách hàng')),
                ('depositamount', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Số tiền gửi')),
                ('withdrawalamount', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Số tiền rút')),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bankbookkk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.bankbookkk', verbose_name='Mã sổ')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('3 tháng', '3 tháng'), ('6 tháng', '6 tháng'), ('Không kỳ hạn', 'Không kỳ hạn')], max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('tags', models.ManyToManyField(to='account.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('amount', models.FloatField(null=True)),
                ('note', models.CharField(max_length=1000, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customer')),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.products')),
            ],
        ),
        migrations.AddField(
            model_name='bankbookkk',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customer'),
        ),
        migrations.AddField(
            model_name='bankbookkk',
            name='types',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.bankbookkktype', verbose_name='Loại tiết kiệm'),
        ),
    ]
