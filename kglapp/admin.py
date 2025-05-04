from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Catergory)
admin.site.register(Stock)
admin.site.register(Sale)
admin.site.register(Procurement)
admin.site.register(Credit)