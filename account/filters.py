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
    type = MultipleChoiceFilter(
        field_name="type",
        choices=(
        ('3 tháng','3 tháng'),
        ('6 tháng','6 tháng'),
        ('Không kỳ hạn','Không kỳ hạn')
        ),
        label=('Loại tiết kiệm:'),
        conjoined=True,
        widget=forms.CheckboxSelectMultiple,
        )
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),

    ]
    #month = CharFilter(field_name='date_created',lookup_expr='icontains')
    month = forms.CharField(widget=forms.Select(choices=MONTH_CHOICES), label="Select a month ")
    # date = DateFilter(field_name="date_created", label=('Ngày:'),
    #                 lookup_expr='contains',
    #                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = BankBookkk
        fields=['type']
        #fields = '__all__'
        #exclude = ['customer','date_created','price','date_created','type']

class DailyFilter(django_filters.FilterSet):
 
    date = DateFilter(field_name="date_created", label=('Ngày:'),
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
