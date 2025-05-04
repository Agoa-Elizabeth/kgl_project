from django.db import models
#borrrowing the functionality of an inbuilt user model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

#from foodapp import views
#from .forms import AddstockForm, AddSaleForm, UpdateStockForm

# Create your models here.

#list of models
  #user table
    #(name, email, phone number, address, gender roles{sales agent, manager, owner})
  #sales table
   #(product name, price, quantity, date of sale, customer name, sales agent name, ) 
  #inventory/stock table
   #(name of product, quantity, price, date of purchase, supplier name, sales agent name)

#user table called Userprofile using Abstractuser from line 3
class Userprofile(AbstractUser):
   is_salesagent = models.BooleanField(default=False)
   is_manager = models.BooleanField(default=False)
   is_owner = models.BooleanField(default=False)
   username = models.CharField(max_length=100, unique=True)
   email = models.EmailField(unique=False, max_length=100)
   phone_number = models.CharField(max_length=25, unique=False)
   address = models.CharField(max_length=255)
   gender = models.CharField(blank= False)
   BRANCH_CHOICES = [
    ('Maganjo', 'Maganjo'),
    ('Matugga', 'Matugga'),
]
   branch_name = models.CharField(max_length=50, default='Matugga', choices=BRANCH_CHOICES)

   # Override default reverse accessors to avoid conflicts
   
   groups = models.ManyToManyField(
      Group,
        related_name="userprofile_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
   user_permissions = models.ManyToManyField(
      Permission,
        related_name="userprofile_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )
  
   def __str__(self):
      return self.username

#convert the userprofile model to a string for easy readability


class Catergory(models.Model):
   catergory_name = models.CharField(max_length=100, blank=False, null=True)
   def __str__(self):
      return self.catergory_name
   
#stock table called stock
class Stock(models.Model):
   catergory_name = models.ForeignKey(Catergory, on_delete = models.CASCADE)
   item_name = models.CharField(max_length=100, blank=True, null=True)
   total_quantity = models.IntegerField(null=True, blank=False, default=0)
   issued_quantity =models.IntegerField(null=True, blank=False, default=0)
   received_quantity = models.IntegerField(null=True, blank=False,default=0)
   supplier_name = models.CharField(max_length=100)
   date_of_purchase = models.DateField(auto_now_add=False)
   type_of_stock = models.CharField(max_length=100, blank=False, null=True)
   unit_price = models.IntegerField(blank=False, default=0, null=True) #cost of the product
   totalcost = models.IntegerField(null=True, blank=False, default=0) #total cost of the product
   sales_agent_name = models.CharField(max_length=100, null=False)
   BRANCH_CHOICES = [
    ('Maganjo', 'Maganjo'),
    ('Matugga', 'Matugga'),
]
   branch_name = models.CharField(max_length=50, default='Majango', choices=BRANCH_CHOICES)


   def __str__(self):
      return self.item_name
   

#sales table called sales
class Sale(models.Model):
   product_name = models.ForeignKey(Stock, on_delete=models.CASCADE) 
   tonnage_kgs = models.IntegerField(default=0, blank=False, null=True)
   #price of the product sold
   unit_price = models.IntegerField(blank=False, default=0, null=True)
   amount_paid_ugx = models.IntegerField(blank=False, default=0, null=True)
   amount_recieved = models.IntegerField(blank=False, default=0, null=True)
   #if the payment is deferred or not
   payment_method = models.CharField(choices=[("Cash","Cash"), ("Credit","Credit")], default=False) 
   customer_name = models.CharField(max_length=100, blank=False, null=True)
   date_time = models.DateTimeField(blank=False, null=True)
   sales_agent_name =  models.CharField(max_length=100, null=False, default='Unknown')



   #calculating the total price of the product sold
   def get_sale(self):
      expected_sale = self.tonnage_kgs * self.product_name.unit_price
      return int(expected_sale)
   
   #calculating the change to be given to the customer
   def get_change(self): 
      #change = amount_recieved - expected_sales
      #total amount received from the customer
      change = self.get_sale() - self.amount_recieved
      #abs is used to get the absolute value of the change
      return abs(int(change))
   
   def total_sale(self):
      total = self.tonnage_kgs * self.product_name.amount_paid
      return int(total)


   def __str__(self):
      return self.customer_name

   #(name of product, quantity, price, date of purchase, supplier name, sales agent name)

class Procurement(models.Model):
   name_of_produce = models.CharField(max_length=100, blank=False, null=False)
   type_of_produce = models.CharField(blank=False)
   date = models.DateField(blank=False, auto_now_add=True)
   tonnage_kg = models.IntegerField(blank=False, null=False)
   cost_ugx = models.IntegerField(blank=False)
   name_of_dealer = models.CharField(blank=False )
   BRANCH_CHOICES = [
    ('Maganjo', 'Maganjo'),
    ('Matugga', 'Matugga'),
]
   branch_name = models.CharField(max_length=50, default='Maganjo', choices=BRANCH_CHOICES)
   contact_of_dealer = models.IntegerField(blank=False)
   selling_price = models.IntegerField(blank=False )
   added_by = models.CharField(blank=False)

   def __str__(self):
        return f"{self.name_of_produce} - {self.branch_name}"

class Credit(models.Model):
    buyer_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=15, blank=False, null=True)
    amount_due_ugx = models.IntegerField(default=0, null=True, blank=True)
    deposit_paid_ugx = models.IntegerField(default=0, null=True, blank=True)  # Added this field
    is_paid = models.BooleanField(default=False, blank=False, null=True)
    sales_agent_name = models.CharField(max_length=100, null=True, blank=True,  default=False)
    due_date = models.DateField()  # Removed auto_now
    produce_name = models.CharField(max_length=100)
    tonnage_kgs = models.IntegerField(default=0)
    date_of_dispatch = models.DateField(auto_now_add=True)

    def balance_due(self):
        return self.amount_due_ugx - self.deposit_paid_ugx
