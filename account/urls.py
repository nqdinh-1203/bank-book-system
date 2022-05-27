from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.loginPage,name='login'),
    path('register/', views.registerPage,name='register'),
    path('logout/', views.logoutUser,name='logout'),

    path('', views.home,name='home'),
    path('user/', views.userPage,name='user-page'),
    path('account/', views.accountSettings,name='account'),
    path('create_bankbook/',views.createBankBook,name='create_bankbook'),
    path('deposit/',views.depositMoney,name='deposit'),
    path('checkout/',views.checkout,name='checkout'),
    path('search1/',views.search1,name='search1'),
    path('search2/',views.search2,name='search2'),
    path('daily/',views.createDailyReport,name='daily'),
    path('monthly/',views.createMonthlyReport,name='monthly'),
    path('products/', views.products,name='products'),
    path('customer/<str:pk_test>/', views.customer,name='customer'),
    path('create_order/<str:pk>',views.createOrder,name='create_order'),
    path('update_order/<str:pk>',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>',views.deleteOrder,name='delete_order'),
    

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
    name='reset_password'),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
    name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
    name='password_reset_confirm'),
    
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
    name='password_reset_complete'),
] 
