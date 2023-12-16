from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(Review)
