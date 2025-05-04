"""
URL configuration for kglproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kglapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    #below is the url for add stock page
    path('addstock/', views.addstock, name='addstock'),


    #below is url showing all records of stock
    path('allstock/', views.allstock, name='allstock'),
   
    #below is the url for  add sales page
    path('addsales/', views.addsales, name='addsales'),

    path('addsales/<int:database_id>/', views.addsales, name='addsales'),
    #below is url showing all records of sales
    path('allsales/', views.allsales, name='allsales'),

    #handling a url for a particular checkout item
    path('allstock/<int:id>/', views.stock_detail, name='stock_detail'),

    #handling a url for a particular sell item
    #path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),
    

    #Receipts
    path('receipt/<int:sale_id>/', views.generate_receipt, name='generate_receipt'),

    #credits
    path('all_credit/', views.all_credit, name='all_credit'),
    path('add_credit/', views.add_credit, name='add_credit'),

    path('', auth_views.LoginView.as_view(template_name='kglapp/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='kglapp/logout.html'), name='logout'),

    path('login/', views.login, name='login'),
    

    path('signup/', views.signup, name='signup'),

    
    path('dashboard2/', views.manager, name='manager'),
    path('dashboard1/', views.owner, name='owner'),

    #owners dashboard
    #path('owner/dashboard/', views.business_owner_dashboard, name='business_owner_dashboard'),

    #sales agent
    path('dashboard3/', views.sales_agent_dashboard, name='dashboard3'),
   



    #url for manager dasboard
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    #path('procurement/', views.procurement_view, name='procurement'),
    path('stock/', views.stock_view, name='stock_view'),
    path('logout/', views.logout_view, name='logout'),


   
    path('procurement/', views.procure_produce, name='procurement'),

    path('stock/', views.stock_view, name='stock'),

   #edit
   path('stock/edit/<int:pk>/', views.edit_stock, name='edit_stock'),

    #delete
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
]
