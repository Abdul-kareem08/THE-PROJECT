from django.db import models
from django.contrib.auth.models import User

# ----------------------

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    business_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    business_id = models.CharField(max_length=100)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name

class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ----------------------
# Buyer Profile
# ----------------------
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile', null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.email


# ----------------------
# Review (Buyer → Seller)
# ----------------------
class Review(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.SET_NULL, related_name='reviews', null=True, blank=True)

    buyer_email = models.EmailField(blank=True, null=True)
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer_name or self.buyer_email} for {self.seller.business_name}"


# ----------------------
# Admin Profile
# ----------------------
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
