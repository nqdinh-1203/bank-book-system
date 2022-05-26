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



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="logo2.png",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY = (
        # ('Indoor','Indoor'),
        # ('Outdoor','Outdoor'),
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
        
def diff_month(d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

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
    balance = models.FloatField(null=True,default=0)

    types = models.ForeignKey(
        BankBookkkType,null=True,
        on_delete=models.CASCADE,
        verbose_name='Loại tiết kiệm'
    )
    #type = models.CharField(max_length=200, null=True,choices=TYPE,verbose_name='Loại tiết kiệm')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if self.balance == 0:
            self.balance = self.firstdeposit
            self.firstdeposit = 0
        super(BankBookkk, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.bookid)
    

    def updateBalance(self):
        
        # created_month = diff_month(timezone.now(), self.date_created)
        created_month = 10
        print(created_month)
        print(self.types.name)
        print(self.types.interest_rate)
        print(self.types.period)
        # s
        if self.types.name == 'Không kỳ hạn':
            print('OK1')
            if created_month >= 1:
                print('OK2')
                print(self.balance)
                self.balance = int(self.balance*float(1+self.types.interest_rate/100)*float(created_month))
                print(self.balance)
                print('OK3')
                self.types.maximum_withdrawal_amount = self.balance
        else:
            print('OK5')
            self.balance = int(self.balance*float(1+self.types.interest_rate/100)*float(created_month//self.types.period)*self.types.period)
            print('OK5')
            self.types.minimum_withdrawal_amount = self.balance
            print('OK6')
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
        null=True,
        default=0,
        decimal_places=2,
        max_digits=12,
        verbose_name='Số tiền gửi'
    )
    withdrawalamount = models.DecimalField(
        null=True,
        default=0,
        decimal_places=2,
        max_digits=12,
        verbose_name='Số tiền rút'
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    # transaction_type = models.PositiveSmallIntegerField(
    #     choices=TRANSACTION_TYPE_CHOICES
    # )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bankbookkk.bookid)

    class Meta:
        ordering = ['timestamp']


# class MonthlyReport(models.Model):
#     TYPE = (
#         ('3 tháng','3 tháng'),
#         ('6 tháng','6 tháng'),
#         ('Không kỳ hạn','Không kỳ hạn'),
#         )
#     type = models.CharField(max_length=200, null=True,choices=TYPE)


# class DailyReport(models.Model):
    
    