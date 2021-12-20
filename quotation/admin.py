from django.contrib import admin
from .models import Company, Category, Item, Current, Inquiry, ItemQuota
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Current)
admin.site.register(Inquiry)
admin.site.register(ItemQuota)

# Register for history
