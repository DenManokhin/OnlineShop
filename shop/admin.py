from django.contrib import admin

from shop.models import Item, OrderItem, Order, Review


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Review)
