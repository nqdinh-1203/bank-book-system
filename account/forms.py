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
        #fielts = [] để chọn ra fields (['customer','product'])




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
    def clean_amount(self):
        bankbookk = self.bankbookk
        min_withdraw_amount = bankbookk.types.minimum_deposit_amount
        max_withdraw_amount = bankbookk.types.maximum_withdrawal_amount

        balance = bankbookk.balance

        amount = self.cleaned_data.get('withdrawalamount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'Bạn cần rút ít nhất {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'Bạn được rút nhiều nhất {max_withdraw_amount} $'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'Bạn có {balance}đ trong tài khoản. '
                'Bạn không rút nhiều hơn số dư trong tài khoản'
            )

        return amount
    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
