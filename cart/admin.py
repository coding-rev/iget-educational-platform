from django.contrib import admin
from .models import OrderItem, Order
# Register your models here.

class AdminOrder(admin.ModelAdmin):
	list_display = ["user", "ordered"]
	list_filter  = ["ordered", "user"]

admin.site.register(OrderItem)
admin.site.register(Order, AdminOrder)
