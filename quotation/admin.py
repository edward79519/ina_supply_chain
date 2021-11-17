from django.contrib import admin
from .models import Company, Category, Item, Current, Inquiry, ItemQuota

# Register your models here.

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Current)
admin.site.register(Inquiry)
admin.site.register(ItemQuota)
