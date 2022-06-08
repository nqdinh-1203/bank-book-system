from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from decimal import Decimal
from django.utils import timezone
from .constant import TRANSACTION_TYPE_CHOICES
import boto3




# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,verbose_name='Tên khách hàng')
    phone = models.CharField(max_length=200, null=True,verbose_name='Số điện thoại khách hàng')
    email = models.CharField(max_length=200, null=True,verbose_name='Email khách hàng')
    profile_pic = models.ImageField(null=True,blank=True,
    default="https://theblues.s3.us-west-2.amazonaws.com/images/benzema_laya.jpeg",
    upload_to='images',
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    identityid = models.CharField(max_length=200, null=True,blank=True,verbose_name='CMND/CCCD')
    address = models.CharField(max_length=200, null=True,blank=True,verbose_name='Địa chỉ')

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY = (
        ('3 tháng','3 tháng'),
        ('6 tháng','6 tháng'),
        ('Không kỳ hạn','Không kỳ hạn')
        )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True,choices=CATEGORY)
    description = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag) 

    def __str__(self):
        return self.name
        

class BankBookkkType(models.Model):
    name = models.CharField(max_length=128,verbose_name='Tên loại tiết kiệm')
    minimum_deposit_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default = 100000,
        verbose_name='Số tiền gửi tối thiểu'
    )
    minimum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        blank=True,null=True,
        help_text='Sẽ được hiệu chỉnh sau',
    )
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        blank=True,null=True,
        help_text='Sẽ được hiệu chỉnh sau',
    )
    #Tỷ lệ lãi suất
    interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Tỷ lệ từ 0 - 100%',
        verbose_name='Tỷ lệ lãi suất'
    )
    # Kỳ hạn của sổ tiết kiệm
    period = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        help_text='Độ dài là 0 tương ứng với Không kỳ hạn',
        verbose_name='Độ dài kỳ hạn '
    )
    def __str__(self):
        return self.name


class BankBookkk(models.Model):
    TYPE = (
        ('3 tháng','3 tháng'),
        ('6 tháng','6 tháng'),
        ('Không kỳ hạn','Không kỳ hạn')
        )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200, null=True,verbose_name='Tên khách hàng')
    identityid = models.CharField(max_length=200, null=True,verbose_name='CMND/CCCD')
    customer_address = models.CharField(max_length=200, null=True,verbose_name='Địa chỉ')
    bookid = models.AutoField(primary_key=True)
    firstdeposit = models.FloatField(null=True,verbose_name='Số tiền gửi')
    balance = models.FloatField(null=True,default=-1)

    types = models.ForeignKey(
        BankBookkkType,null=True,
        on_delete=models.CASCADE,
        verbose_name='Loại tiết kiệm'
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_delete = models.BooleanField(default=False,verbose_name='Sổ đã đóng hay chưa?')

    
    def save(self, *args, **kwargs):
        if self.balance == -1:
            print(self.firstdeposit)
            self.balance = self.firstdeposit
            self.firstdeposit = 0
            print(self.balance)
            print(self.firstdeposit)
        super(BankBookkk, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.bookid)
    

    def updateBalance(self):
        
        #created_month = 2
        import datetime
        naive = datetime.datetime(2023, 5, 26)
        date_created = datetime.datetime.strptime(str(self.date_created.date()), "%Y-%m-%d")
        time_valid = naive - date_created
        created_month = (time_valid // 30).days

        if self.types.name == 'Không kỳ hạn':
            if created_month >= 1:
                self.balance = int(self.balance*float(1+self.types.interest_rate/100)*float(created_month))
                self.types.maximum_withdrawal_amount = self.balance
        else:
            self.balance = int(self.balance*float(1+self.types.interest_rate/100)*float(created_month// self.types.period)*self.types.period)
            self.types.minimum_withdrawal_amount = self.balance
            self.types.maximum_withdrawal_amount = self.balance



class Orders(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        )
    customer = models.ForeignKey(Customer,null=True,on_delete = models.SET_NULL)
    products = models.ForeignKey(Products,null=True,on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True,choices=STATUS)
    amount = models.FloatField(null=True)
    note = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.products.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    first_name=models.CharField(max_length=200,null=True,blank=True)
    last_name=models.CharField(max_length=200,null=True,blank=True)
    phone=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.first_name 


class Transaction(models.Model):
    bankbookkk = models.ForeignKey(
        BankBookkk,
        on_delete=models.CASCADE,
        verbose_name='Mã sổ',
    )
    customer_name = models.CharField(max_length=200, null=True,verbose_name='Tên khách hàng')
    
    depositamount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name='Số tiền gửi',
        null=True,
        default=0
    )
    withdrawalamount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name='Số tiền rút',
        null=True,
        default=0
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bankbookkk.bookid) 

    def save(self, *args, **kwargs):
        self.balance_after_transaction = 0
        super(Transaction, self).save(*args, **kwargs)


    