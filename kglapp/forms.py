from django.forms import ModelForm
#accesing our models to corresponding forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

#creating a form that called addForm
class AddStockForm(ModelForm):
   class Meta:
      model = Stock
      fields = '__all__'

class AddSaleForm(ModelForm):
   class Meta:
      model = Sale
      fields = '__all__'

class UpdateStockForm(ModelForm):
   class Meta:
      model = Stock
      fields =  ['received_quantity']

from django import forms
from .models import Credit

class AddCreditForm(ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'
      

class UserCreation(UserCreationForm):
   class Meta:
      model = Userprofile
      fields =  '__all__'
   def save(self, commit=True):
      user = super(UserCreation, self).save(commit=False)
      if commit:
         user.is_activate = True
         user.is_staff = True
         user.save()
      return user
   
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__' 


class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = '__all__' 

        #edit
        