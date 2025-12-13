"""
URL configuration for kgl_project project.

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from kglapp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('favicon.ico', serve, {'document_root': settings.STATIC_ROOT, 'path': 'images/logo-1.png'}),
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('addstock/', views.addstock, name='addstock'),
    path('allstock/', views.allstock, name='allstock'),
    path('addsales/', views.addsales, name='addsales'),
    path('addsales/<int:database_id>/', views.addsales, name='addsales_with_id'),
    path('allsales/', views.allsales, name='allsales'),
    path('allstock/<int:id>/', views.stock_detail, name='stock_detail'),
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),
    path('receipt/<int:sale_id>/', views.generate_receipt, name='generate_receipt'),
    path('all_credit/', views.all_credit, name='all_credit'),
    path('add_credit/', views.add_credit, name='add_credit'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard1/', views.owner, name='dashboard1'),
    path('dashboard2/', views.manager, name='dashboard2'),
    path('dashboard3/', views.sales_agent_dashboard, name='dashboard3'),
    path('procurement/', views.procure_produce, name='procurement'),
    path('stock/', views.stock_view, name='stock'),
    path('stock/edit/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
