from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from django.conf import settings
from django.db.models import Q
from django.forms import BaseFormSet


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'

class BankBookForm(ModelForm):
    class Meta:
        model = BankBookkk
        fields = [
            'types','customer_name','identityid',
            'customer_address','firstdeposit'
        ]

class DepositForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'bankbookkk',
            'customer_name',
            'depositamount',
        ]
    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('instance')
        criterion1 = Q(customer=customer)
        criterion2 = Q(is_delete=False)
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['bankbookkk'].queryset = BankBookkk.objects.filter(criterion1 & criterion2)


class WithdrawForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'bankbookkk',
            'customer_name',
            'withdrawalamount',
        ]    
    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('instance')
        criterion1 = Q(customer=customer)
        criterion2 = Q(is_delete=False)
        super(WithdrawForm, self).__init__(*args, **kwargs)
        self.fields['bankbookkk'].queryset = BankBookkk.objects.filter(criterion1 & criterion2)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
