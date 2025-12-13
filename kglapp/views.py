from django.shortcuts import render, redirect
from .models import *  
from .forms import *    
from django.urls import reverse
from django.http import *
from django.shortcuts import render, get_object_or_404, redirect
#salesagent dashboard
from django.utils import timezone  # adjust if in different app
from datetime import datetime
from django.db.models.functions import TruncDate
from django.db.models import Sum
from datetime import date
today = date.today()

#credits
from django.contrib import messages


#borrowing decorators from django so that we can retrict viws
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils.timezone import now



# Create your views here.

def index(request):
   return render(request, 'index.html')

#views for addstock
def addstock(request):
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allstock')  # Change this to wherever you want to redirect after saving
    else:
        form = AddStockForm()
    context = {
        'form': form
    }
    return render(request, 'addstock.html', context)


def allstock(request):
     stocks = Stock.objects.all().order_by('-id')
     return render(request, 'allstock.html',{'stocks':stocks})

def addsales(request):
    form = AddSaleForm()
    return render(request, 'issue_item.html', {'form':form})

def allsales(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'allsales.html', {'sales': sales})

def stock_detail(request, id):
    # Get the stock item by its ID
    stock = Stock.objects.get(id=id)
    return render(request, 'stock_detail.html', {'stock': stock})



def issue_item(request, pk=None):  # Make pk optional
    if pk:
        issued_item = get_object_or_404(Stock, pk=pk)
    else:
        # Handle case where no item is selected (redirect or show form)
        return redirect('allstock')  # Redirect to stock list

    if request.method == 'POST':
        sales_form = AddSaleForm(request.POST)
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.item_name = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()

            # Update stock quantity
            issued_quantity = sales_form.cleaned_data.get('quantity', 0)
            issued_item.total_quantity -= issued_quantity
            issued_item.save()

            return redirect('allsales')
    else:
        # Pre-fill form with initial data
        sales_form = AddSaleForm(initial={
            'item_name': issued_item.item_name,
            'unit_price': issued_item.unit_price
        })

    return render(request, 'issue_item.html', {
        'sales_form': sales_form,
        'item': issued_item
    })
def generate_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    context = {
        'customer_name': sale.customer_name,
         'product_name': sale.product_name,
        'tonnage_kgs': sale.tonnage_kgs,
        'payment_method': sale.payment_method,
        'amount_received': sale.amount_recieved,
        'sales_agent_name': sale.sales_agent_name,
        'date': sale.date_time,
    }
    return render(request, 'receipt.html', {'sale': sale})

def all_credit(request):
    credits = Credit.objects.all()
    return render(request, 'all_credit.html', {'credits': credits})

def add_credit(request):
    if request.method == 'POST':
        form = AddCreditForm(request.POST)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.approved_by = request.user
            credit.save()
            messages.success(request, 'Credit added successfully!')
            return redirect('manage_credits')
    else:
        form =AddCreditForm()
    return render(request, 'add_credit.html', {'form': form})




#login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_salesagent:
                    auth_login(request, user)
                    return redirect('dashboard3')
                elif user.is_manager:
                    auth_login(request, user)
                    return redirect('dashboard2')
                elif user.is_owner:
                    auth_login(request, user)
                    return redirect('dashboard1')
                else:
                    messages.error(request, 'Your account does not have the required permissions.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'Login'})

def manager(request):
    return render(request, "dashboard2.html")

def owner(request):
    return render(request, "dashboard1.html")

#view for signing up
def signup(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            return redirect('login')
    else:
        form = UserCreation()
    return render(request, 'signup.html', {'form': form})


#views for owners dashboard


#views for sales agent dashboard
def is_sales_agent(user):
    return user.groups.filter(name='SalesAgent').exists()

#Managr dashboard
#@login_required
def dashboard2(request):
    return render(request, 'kglapp/dashboard2.html')

#@login_required
def manager_dashboard(request):
    return render(request, 'kglapp/manager_dashboard.html')

#@login_required
def procurement_view(request):
    return render(request, 'kglapp/procurement.html')

#@login_required
def stock_view(request):
    return render(request, 'kglapp/stock.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # adjust 'login' to match your actual login URL name


#sales agent dashboard
#@login_required(login_url='login')  # Redirect to your login page if not authenticated
def sales_agent_dashboard(request): 
    user = request.user
    today = now().date()

    # Filter today's sales using TruncDate for compatibility
    today_sales = Sale.objects.annotate(date_only=TruncDate('date_time'))\
                          .filter(sales_agent_name=user, date_only=today)

    # Calculate total sales today
    total_sales_today = sum(sale.amount_paid_ugx for sale in today_sales)

    # Count unique buyers served today
    buyers_count = today_sales.values('customer_name').distinct().count()

    # Total credit sales by this agent
    credit_sales = Credit.objects.filter(sales_agent_name=user.username)
    credit_sales_total = sum(credit.amount_due_ugx for credit in credit_sales)

    # Recent sales (limit to 10 latest)
    recent_sales_qs = Sale.objects.filter(sales_agent_name=user).order_by('-date_time')[:10]

    recent_sales = [
        {
            'date': sale.date_time.strftime('%Y-%m-%d %H:%M'),
            'produce_name': sale.product_name.item_name if sale.product_name else 'N/A',
            'buyer_name': sale.customer_name,
            'tonnage': sale.tonnage_kgs,
            'amount': sale.amount_paid_ugx,
            'payment_type': sale.payment_method
        }
        for sale in recent_sales_qs
    ]

    context = {
        'total_sales_today': total_sales_today,
        'buyers_count': buyers_count,
        'credit_sales_total': credit_sales_total,
        'recent_sales': recent_sales
    }

    return render(request, 'dashboard3.html', context)

def allsale():
    return render(request, 'allsale')

#def all_credit():
    #return render(request, 'all_credit')

#def add_credit():
   # return render(request, add_credit)
  

def delete_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        stock.delete()
    return redirect('stock_page')

#Manager dashboard
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

#@user_passes_test(is_manager)
def procure_produce(request):
      if request.method == 'POST':
        form = ProcurementForm(request.POST)
        if form.is_valid():
            procurement = form.save(commit=False)
            procurement.added_by = request.user
            procurement.save()
            messages.success(request, "Produce successfully procured and recorded.")
            return redirect('procurement')  
        else:
            messages.error(request, "Please fill in the correct information")
      else:
        form = ProcurementForm()

      procurements = Procurement.objects.all().order_by('-date')
     
      return render(request, 'procurement.html', {
          'form': form,
           'procurements': procurements,
          })
    
#@login_required
def stock_view(request):
    return render(request, 'allstock.html')

#edit
def edit_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('allstock')  # Redirect to stock list after edit
    else:
        form = StockForm(instance=stock)
    
    return render(request, 'edit_stock.html', {'form': form, 'stock': stock})


#delete func
def delete_stock(request, stock_id): 
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
        return redirect('allstock')  # change if your stock list URL has a different name
    return render(request, 'delete_stock.html', {'item': stock})


"""#dashboard1
def dashboard1(request):
   total_sales = Sale.objects.aggregater(payment_method='Cash').aggregate(
        total_cash=Sum('amount_recieved')
    )['total_cash'] or 0

    # 2. Total Credit Sales
   total_credit_sales = Credit.objects.aggregate(
        total_credit=Sum('amount_due_ugx')
    )['total_credit'] or 0

    # 3. Total Sales = Cash + Credit
   total_sales = int(total_cash_sales) + int(total_credit_sales)

    # 4. Total Stock Remaining
   total_stock = Stock.objects.aggregate(
        total_quantity=Sum('total_quantity')
    )['total_quantity'] or 0
   
   # 5. total procurement
   total_procurement = Procurement.objects.aggregate(
    total=Sum('cost_ugx')
    )['total'] or 0

   context = {
        'total_sales': total_sales,
        'total_credit_sales': total_credit_sales,
        'total_stock': total_stock,
        'total_cash_sales': total_cash_sales,
        'total_procurement': total_procurement,
   }
   print("Context being sent to template:", context)
   
   return render(request, 'dashboard1.html', context)"""

def owner (request):
    # Total Sales
    total_sales = Sale.objects.aggregate(total=Sum('amount_paid_ugx'))['total'] or 0

    # Total Procurements
    total_procurement = Procurement.objects.aggregate(total=Sum('tonnage_kg'))['total'] or 0

    # Total Stock
    total_stock = Stock.objects.aggregate(total=Sum('total_quantity'))['total'] or 0

    # Total Credit Sales
    total_credit_sales = Credit.objects.aggregate(total=Sum('amount_due_ugx'))['total'] or 0

    context = {
        'total_sales': total_sales,
        'total_procurement': total_procurement,
        'total_stock': total_stock,
        'total_credit_sales': total_credit_sales,
    }

    print("Total Sales:", total_sales)

    return render(request, 'dashboard1.html', context)