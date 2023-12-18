from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Item)
admin.site.register(Users)
admin.site.register(categories)
admin.site.register(interaction)
admin.site.register(checkout)
admin.site.register(orders)
admin.site.register(orderdetails)
admin.site.register(productsrequests)
