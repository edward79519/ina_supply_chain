from django.contrib import admin
from .models import Company, Category, Item

# Register your models here.

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Item)
