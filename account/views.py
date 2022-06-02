from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Sum,Count
from numpy import identity
from django import forms
from django.utils import timezone
from .models import *


from account.decorators import unauthenticated_user 

# Create your views here.
from .models import *
from .forms import  OrderForm, CreateUserForm,CustomerForm,DepositForm,WithdrawForm
from .filters import OrderFilter,MonthlyFilter,DailyFilter,Search
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm(request.POST)
    if request.method == 'POST':
        print('Printing POST: ',request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for ' + username)

            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None: 
            login(request, user)
            return redirect('home')
        else:   
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Orders.objects.all() 
    customers = Customer.objects.all()
    
    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers': customers,
    'total_customers':total_customers,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.orders_set.all()
    bankbooks =  request.user.customer.bankbookkk_set.all().filter(is_delete=False)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('ORDERS:',orders)
    print('BANKBOOKS:',bankbooks)
    
    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending,'bankbooks':bankbooks}
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form} 
    return render(request, 'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createBankBook(request):
    customer = request.user.customer

    OrderFormSet = inlineformset_factory(Customer, BankBookkk, fields=('types','customer_name','identityid',
                                                                     'customer_address','firstdeposit',
                                                                     ),extra=1,can_delete=False
                                                                    #  ,initial=[{'date_created':timezone.now(),}]
                                                                     )
    formset = OrderFormSet(queryset=BankBookkk.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            money = formset.cleaned_data[0]['firstdeposit']
            if money >= 100000:
                
                bankbookkks = formset.save()
                bankbookkk = bankbookkks[0]
                Transaction.objects.create(bankbookkk=bankbookkk,
                                                        depositamount = money,
                                                        customer_name=formset.cleaned_data[0]['customer_name'])
                return redirect('/')
            else: 
                messages.info(request, 'Số tiền gửi tối thiếu là 100,000')
                
    context = {'formset':formset} 
    return render(request, 'accounts/bankbook_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.orders_set.all()
    orders_count= orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    
    amounts = orders.values('status').annotate(entries=Sum('amount'))
    context = {'customer':customer,'orders':orders,'orders_count':orders_count,
    'myFilter':myFilter,'amounts':amounts}

    return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        print('Printing POST: ',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, BankBookkk, fields=('type','customer_name','identityid',
                                                                    'customer_address','firstdeposit',
                                                                    ),extra=1)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=BankBookkk.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def depositMoney(request):

    customer = request.user.customer
    form = DepositForm(instance=customer)
    if request.method == 'POST':
        form = DepositForm(request.POST,instance=customer)
        if form.is_valid():
            amount = form.cleaned_data.get('depositamount')
            id = form.cleaned_data.get('bankbookkk')

            from django.db.models import Q
            criterion1 = Q(customer=customer)
            criterion2 = Q(bookid=str(id))

            bankbookkk = BankBookkk.objects.filter(criterion1 & criterion2).first()
            
            if bankbookkk.types.period == 0:

                bankbookkk.updateBalance()

                min_deposit_amount = bankbookkk.types.minimum_deposit_amount
                if amount < min_deposit_amount:
                    messages.success(request, f'Bạn cần gửi tối thiểu {min_deposit_amount} ')
                else:
                    bankbookkk.balance = Decimal(bankbookkk.balance) + amount
                    deposit = Transaction.objects.create(bankbookkk=bankbookkk,
                                                        depositamount = amount,
                                                        customer_name=form.cleaned_data.get('customer_name'))
                    
                    bankbookkk.save(
                        update_fields=['balance']
                    )
                    return redirect('/')
            else:
                messages.info(request, 'Chỉ nhận gởi tiền với loại tiết kiệm không kỳ hạn.')

    context = {'form':form}
    return render(request, 'accounts/deposit_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def withdrawMoney(request):

    customer = request.user.customer
    form = WithdrawForm(instance=customer)
    if request.method == 'POST':
        form = WithdrawForm(request.POST,instance=customer)
        if form.is_valid():
            amount = form.cleaned_data.get('depositamount')
            id = form.cleaned_data.get('bankbookkk')

            from django.db.models import Q
            criterion1 = Q(customer=customer)
            criterion2 = Q(bookid=str(id))

            bankbookkk = BankBookkk.objects.filter(criterion1 & criterion2).first()
            bankbookkk.updateBalance()
            print(bankbookkk)
            created_days = (timezone.now() - bankbookkk.date_created).days
            created_months = (timezone.now() - bankbookkk.date_created).months
            print(created_days,created_months)
            if created_days < 15:
                messages.success(request, f'Chỉ được rút tiền khi mở sổ ít nhất 15 ngày')
                return

            if bankbookkk.types.period != 0:
                if created_months < bankbookkk.types.period:
                    messages.success(request, f'Loại tiết kiệm có kỳ hạn chỉ đưọc rút khi quá kỳ hạn')
                    return

            min_withdrawal_amount = bankbookkk.types.minimum_withdrawal_amount
            max_withdrawal_amount = bankbookkk.types.maximum_withdrawal_amount

            if amount < min_withdrawal_amount:
                messages.success(request, f'Bạn cần rút tối thiểu {min_withdrawal_amount}')
            elif amount > max_withdrawal_amount:
                messages.success(request, f'Bạn chỉ được rút tối đa {max_withdrawal_amount}')
            else:
                bankbookkk.balance = Decimal(bankbookkk.balance) - amount
                bankbookkk.save(
                    update_fields=['balance']
                )
                return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/withdraw_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    customer = request.user.customer
    form = WithdrawForm(instance=customer)
    if request.method == 'POST':
        form = WithdrawForm(request.POST,instance=customer)
        if form.is_valid():
            amount = form.cleaned_data.get('withdrawalamount')
            id = form.cleaned_data.get('bankbookkk')

            from django.db.models import Q
            criterion1 = Q(customer=customer)
            criterion2 = Q(bookid=str(id))

            bankbookkk = BankBookkk.objects.filter(criterion1 & criterion2).first()
            
            if bankbookkk.balance == 0:
                messages.success(request, f'Sổ đã đóng')
                context = {'form':form}
                return render(request, 'accounts/checkout.html', context)


            import datetime

            naive = datetime.datetime(2020, 5, 17)
            now = datetime.datetime.now()

            time_extract = now - naive

            if time_extract.days >= 15:
                
                bankbookkk.updateBalance()
                min_money_checkout = bankbookkk.types.minimum_withdrawal_amount
                max_money_checkout = bankbookkk.types.maximum_withdrawal_amount

                # print(bankbookkk.types.name, min_money_checkout, max_money_checkout, bankbookkk.balance)
                flag = 0
                if bankbookkk.types.name != 'Không kỳ hạn':
                    naive = datetime.datetime(2023, 5, 26)
                    date_created = datetime.datetime.strptime(str(bankbookkk.date_created.date()), "%Y-%m-%d")
                    time_valid = naive - date_created
                    # print(naive.date(), date_created.date(), time_valid)
                    if time_valid.days < int(bankbookkk.types.period)*30:
                        flag = 1
                        messages.success(request, f'Bạn chưa tới kì hạn {bankbookkk.types.period} tháng')
                if flag == 0:
                    if amount < min_money_checkout:
                        messages.success(request, f'Bạn cần rút tối thiểu {min_money_checkout} ')
                    elif amount > max_money_checkout:
                        messages.success(request, f'Bạn cần rút tối đa {max_money_checkout} ')
                    else:
                        bankbookkk.balance = Decimal(bankbookkk.balance) - amount
                        bankbookkk.save(
                            update_fields=['balance']
                        )
                        Transaction.objects.create(bankbookkk=bankbookkk,
                                                        withdrawalamount = amount,
                                                        customer_name=form.cleaned_data.get('customer_name'))
                        print(bankbookkk.balance)
                        if bankbookkk.balance == 0:
                           
                            #bankbookkk.delete()
                            bankbookkk.is_delete = True
                            bankbookkk.save(
                                update_fields=['is_delete']
                            )
                        return redirect('/')
            else:
                messages.info(request, 'Sổ phải mở ít nhất 15 ngày.')
    context = {'form':form}
    return render(request, 'accounts/checkout.html', context)


    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def search1(request):

    bankbooks =  request.user.customer.bankbookkk_set.all()
    myFilter = Search(request.GET, queryset=bankbooks)
    bankbookres= myFilter.qs
    
    context = {'bankbooks':bankbooks,'bankbookres':bankbookres,'myFilter':myFilter}


    return render(request,'accounts/search.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search2(request):

    bankbooks =  BankBookkk.objects.all()
    myFilter = Search(request.GET, queryset=bankbooks)
    bankbookres= myFilter.qs
    
    context = {'bankbooks':bankbooks,'bankbookres':bankbookres,'myFilter':myFilter}


    return render(request,'accounts/search.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createDailyReport(request):

    transactions = Transaction.objects.all()
    myFilter = DailyFilter(request.GET, queryset=transactions)
    transactionres= myFilter.qs

    results = transactionres.values('bankbookkk__types__name').annotate(deposit=Sum('depositamount'),
                                                                        withdraw=Sum('withdrawalamount'),
                                                                        diff=Sum('depositamount')-Sum('withdrawalamount'))

    context = {'transactions':transactions,'transactionres':transactionres,'myFilter':myFilter,'results':results}

    return render(request,'accounts/daily.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createMonthlyReport(request):

    transactions = Transaction.objects.all()
    myFilter = MonthlyFilter(request.GET, queryset=transactions)
    transactionres= myFilter.qs

    from django.db.models import Q
    results = transactionres.extra(select={'day': 'date(timestamp)'})\
                            .values('day')\
                            .annotate(open=Count('bankbookkk__bookid',distinct=True),
                                    closed=Count('bankbookkk__is_delete',only=Q(bankbookkk__is_delete=True)),
                                    diff=Count('bankbookkk__bookid',distinct=True)-Count('bankbookkk__is_delete',only=Q(bankbookkk__is_delete=True))
                                    )
    

    context = {'transactions':transactions,'transactionres':transactionres,'myFilter':myFilter,'results':results}

    return render(request,'accounts/monthly.html',context)

    
