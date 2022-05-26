from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Sum
from numpy import identity
from django import forms
from django.utils import timezone


from account.decorators import unauthenticated_user 

# Create your views here.
from .models import *
from .forms import  OrderForm, CreateUserForm,CustomerForm,DepositForm,WithdrawForm
from .filters import OrderFilter,MonthlyFilter,DailyFilter
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
    bankbooks = 1
    bankbooks =  request.user.customer.bankbookkk_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('ORDERS:',orders)
    print('BANKBOOKS:',bankbooks)
    
    # for i in bankbooks:
    #     print(i['amount'])
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
                print('OK')
                formset.save()
                return redirect('/')
            else: 
                print('Not OK')
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

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createOrder(request,pk):
#     OrderFormSet = inlineformset_factory(Customer, Orders, fields=('products','status','amount'),extra=5)
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet(queryset=Orders.objects.none(),instance=customer)
#     #form = OrderForm(initial={'customer':customer})
#     if request.method == 'POST':
#         #print('Printing POST: ',request.POST)
#         #form = OrderForm(request.POST)
#         formset = OrderFormSet(request.POST,instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('/')
#     context = {'formset': formset}
#     return render(request,'accounts/order_form.html',context)

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
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST: ',request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request,'accounts/order_form.html',context)

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
@allowed_users(allowed_roles=['customer'])
def depositMoney(request):

    customer = request.user.customer
    #bankbook = BankBookkk.objects.get(bookid=pk)
    form = DepositForm(instance=customer)
    if request.method == 'POST':
        form = DepositForm(request.POST,instance=customer)
        if form.is_valid():
            amount = form.cleaned_data.get('depositamount')
            # print(amount)
            # print(type(amount))
            id = form.cleaned_data.get('bankbookkk')
            # print(id)
            #customer = request.user.customer
            #print(Customer.objects.filter(user=request.user).all().values())
            #print(BankBookkk.objects.all().values())
            #print(type(id))
            from django.db.models import Q
            criterion1 = Q(customer=request.user.customer)
            criterion2 = Q(bookid=str(id))
            # print(BankBookkk.objects.filter(criterion1 & criterion2).all().values())
            bankbookkk = BankBookkk.objects.filter(criterion1 & criterion2).first()
            # print(bankbookkk)
            # print(type(bankbookkk))
            bankbookkk.updateBalance()
            # print(bankbookkk.balance)
            bankbookkk.balance = Decimal(bankbookkk.balance) + amount
            # print(bankbookkk.balance)
            bankbookkk.save(
                update_fields=['balance']
            )
            # print(bankbookkk.balance)
            bankbooks =  request.user.customer.bankbookkk_set.all().values()
            # print(bankbooks)
            messages.success(
            request,
            f'{amount}$ was deposited to your account successfully'
            )
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/deposit_form.html',context)


# class WithdrawMoneyView(TransactionCreateMixin):
#     form_class = WithdrawForm
#     title = 'Withdraw Money from Your Account'

#     def get_initial(self):
#         initial = {'transaction_type': WITHDRAWAL}
#         return initial

#     def form_valid(self, form):
#         amount = form.cleaned_data.get('amount')

#         self.request.user.account.balance -= form.cleaned_data.get('amount')
#         self.request.user.account.save(update_fields=['balance'])

#         messages.success(
#             self.request,
#             f'Successfully withdrawn {amount}$ from your account'
#         )

#         return super().form_valid(form)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createMonthlyReport(request,pk_test):
#     customer = Customer.objects.get(id=pk_test)

#     orders = customer.orders_set.all()
#     orders_count= orders.count()
#     bank_books = customer.bank_book_set.all()
#     bank_book_count= bank_books.count()
    

#     myFilter = MonthlyFilter(request.GET, queryset=bank_books)
#     bank_books = myFilter.qs

#     bank_books = bank_books.filter

#     context = {'customer':customer,'orders':orders,'orders_count':orders_count,
#     'myFilter':myFilter}
#     return render(request, 'accounts/customer.html',context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createDailyReport(request,pk):
#     OrderFormSet = inlineformset_factory(Customer, Orders, fields=('products','status'),extra=5)
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet(queryset=Orders.objects.none(),instance=customer)
#     if request.method == 'POST':
#         formset = OrderFormSet(request.POST,instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('/')
#     context = {'formset': formset}
#     return render(request,'accounts/order_form.html',context)
    