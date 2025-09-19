from django.contrib import admin
from .models import SellerProfile, BuyerProfile, Review, AdminProfile

admin.site.register(SellerProfile)
admin.site.register(BuyerProfile)
admin.site.register(Review)
admin.site.register(AdminProfile)

