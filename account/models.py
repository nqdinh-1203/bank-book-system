from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

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
class BankBook(models.Model):
    TYPE = (
        ('3 tháng','3 tháng'),
        ('6 tháng','6 tháng'),
        ('Không kỳ hạn','Không kỳ hạn')
        )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200, null=True,verbose_name='Tên khách hàng')
    identityid = models.CharField(max_length=200, null=True,verbose_name='CMND/CCCD')
    customer_address = models.CharField(max_length=200, null=True,verbose_name='Địa chỉ')
    #bookid = models.CharField(max_length=200, null=True,blank=True)
    id = models.AutoField(primary_key=True)
    firstdeposit = models.FloatField(null=True,verbose_name='Số tiền gửi')
    balance = models.FloatField(null=True,default=0)
    type = models.CharField(max_length=200, null=True,choices=TYPE,verbose_name='Loại tiết kiệm')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return self.name
 
    def save(self, *args, **kwargs):
        self.balance = self.firstdeposit
 

        super(BankBook, self).save(*args, **kwargs)

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

# class MonthlyReport(models.Model):
#     TYPE = (
#         ('3 tháng','3 tháng'),
#         ('6 tháng','6 tháng'),
#         ('Không kỳ hạn','Không kỳ hạn'),
#         )
#     type = models.CharField(max_length=200, null=True,choices=TYPE)


# class DailyReport(models.Model):
    
    