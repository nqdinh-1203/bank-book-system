from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from django.conf import settings




class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'



class DepositForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'bankbookkk',
            'customer_name',
            'depositamount',
        ]


class WithdrawForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'bankbookkk',
            'customer_name',
            'withdrawalamount',
        ]    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
