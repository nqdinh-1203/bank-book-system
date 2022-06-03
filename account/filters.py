from calendar import c
from django import forms
from warnings import filters
import django_filters 
from django_filters import DateFilter,CharFilter,ModelMultipleChoiceFilter,MultipleChoiceFilter,DateFromToRangeFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        )
    status = MultipleChoiceFilter(
        field_name="status",
        choices=STATUS,
        label=('Loại tiết kiệm:'),
        conjoined=False,
        widget=forms.CheckboxSelectMultiple,
        )
    month = CharFilter(field_name="date_created", label=('Tháng:'),
                    lookup_expr='icontains',
                    widget=forms.DateInput(attrs={'type': 'month'})
                    )
    day = DateFilter(field_name="date_created", label=('Ngày:'),
                    lookup_expr='contains',
                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Orders
        fields = '__all__'
        exclude = ['customer','products','date_created','note']



class MonthlyFilter(django_filters.FilterSet):
    type = ModelMultipleChoiceFilter(
        field_name="bankbookkk__types",
        queryset=BankBookkkType.objects.all(),
        label=('Loại tiết kiệm:'),
        conjoined=False,
        widget=forms.CheckboxSelectMultiple,
        )

    month = CharFilter(field_name="timestamp", label=('Tháng:'),
                    lookup_expr='icontains',
                    widget=forms.DateInput(attrs={'type': 'month'})
                    )
    class Meta:
        model = BankBookkk
        fields=['types']
        exclude = ['types']


class DailyFilter(django_filters.FilterSet):
 
    date = DateFilter(field_name="timestamp", label=('Ngày:'),
                    lookup_expr='contains',
                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = BankBookkk
        fields = ['date_created']
        exclude = ['date_created']


    
class Search(django_filters.FilterSet):
    date = DateFilter(field_name="date_created", label=('Ngày:'),
                    lookup_expr='contains',
                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = BankBookkk
        fields = '__all__'
        exclude = ['firstdeposit','balance','date_created']

class BookFilter(django_filters.FilterSet):
    date = DateFilter(field_name="date_created", label=('Từ ngày:'),
                    lookup_expr='gte',
                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = BankBookkk
        fields = ['bookid', 'types']