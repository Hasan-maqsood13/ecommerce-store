from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Registration)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)