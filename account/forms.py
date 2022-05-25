from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']
class BankbookForm(ModelForm):
    class Meta:
        model=BankBook
        fields='__all__'
        exclude=['customer','amount','date_created','bookid']

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
        #fielts = [] để chọn ra fields (['customer','product'])

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
