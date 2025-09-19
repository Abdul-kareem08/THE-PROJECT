from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import SellerProfile, BuyerProfile, AdminProfile, Review, Product
from rest_framework_simplejwt.tokens import RefreshToken

# ----------------------------
# Seller Registration Serializer
# ----------------------------
class SellerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    is_verified = serializers.BooleanField(read_only=True)  # approval status

    class Meta:
        model = SellerProfile
        fields = [
            "business_name",
            "owner_name",
            "phone_number",
            "business_id",
            "address",
            "email",
            "password",
            "confirm_password",
            "user_email",
            "user_id",
            "is_verified",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(username=attrs.get("email")).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = User.objects.create_user(username=email, email=email, password=password)
        seller = SellerProfile.objects.create(user=user, **validated_data)
        return seller


# ----------------------------
# Seller Login Serializer
# ----------------------------
class SellerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"error": "No seller found with this email."})
        user_auth = authenticate(username=user.username, password=password)
        if not user_auth:
            raise serializers.ValidationError({"error": "Invalid password."})
        if not hasattr(user, "seller_profile"):
            raise serializers.ValidationError({"error": "This user is not a registered seller."})
        attrs["user"] = user
        attrs["seller_profile"] = user.seller_profile
        return attrs


# ----------------------------
# Seller Serializer
# ----------------------------
class SellerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = SellerProfile
        fields = "__all__"
        
        
class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"


# ----------------------------
# Product Serializer
# ----------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["seller"]


# ----------------------------
# Review Serializer
# ----------------------------
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


# ----------------------------
# Admin Login Serializer
# ----------------------------
class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user or not hasattr(user, "admin_profile"):
            raise serializers.ValidationError("Invalid credentials or not an admin.")

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        attrs["user"] = user
        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)
        return attrs


# ----------------------------
# Public Seller Serializer (for listing verified/pending sellers)
# ----------------------------
class PublicSellerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = SellerProfile
        fields = [
            "business_name",
            "owner_name",
            "email",
            "address",
            "is_verified",
        ]
        read_only_fields = fields
