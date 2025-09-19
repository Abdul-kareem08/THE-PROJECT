from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import SellerProfile
from .serializers import (
    SellerRegisterSerializer,
    SellerLoginSerializer,
    SellerSerializer,
    AdminLoginSerializer,
    PublicSellerSerializer,
)

# ----------------------------
# Home / Root view
# ----------------------------
def home(request):
    return HttpResponse("Welcome to the Verified Seller System!")


# ----------------------------
# Seller Registration
# ----------------------------
class SellerRegisterView(generics.CreateAPIView):
    serializer_class = SellerRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller = serializer.save()
        return Response({
            "message": "Seller registered successfully.",
            "seller": SellerSerializer(seller).data,
        }, status=status.HTTP_201_CREATED)


# ----------------------------
# Seller Login
# ----------------------------
class SellerLoginView(generics.GenericAPIView):
    serializer_class = SellerLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller = serializer.validated_data["seller_profile"]
        return Response({
            "message": "Login successful.",
            "seller": SellerSerializer(seller).data,
        }, status=status.HTTP_200_OK)


# ----------------------------
# Pending Sellers
# ----------------------------
class PendingSellersView(generics.ListAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SellerProfile.objects.filter(is_verified=False)


# ----------------------------
# Verified Sellers


class VerifiedSellersView(generics.ListAPIView):
    """
    Returns all sellers who are verified.
    Accessible without login (buyer can view).
    """
    serializer_class = PublicSellerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SellerProfile.objects.filter(is_verified=True)


# ----------------------------
# Approve Seller
# ----------------------------
class ApproveSellerView(generics.UpdateAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return SellerProfile.objects.all()

    def patch(self, request, *args, **kwargs):
        seller = self.get_object()
        seller.is_verified = True
        seller.save()
        return Response({
            "message": f"Seller '{seller.business_name}' approved successfully.",
            "seller": SellerSerializer(seller).data,
        }, status=status.HTTP_200_OK)


# ----------------------------
# Seller Notifications
# ----------------------------
class SellerNotificationsView(generics.ListAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SellerProfile.objects.filter(notified=False)


from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import SellerProfile

# ----------------------------
# Product Upload
# ----------------------------
class ProductUploadView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        # Check if user has seller profile and is approved
        if not hasattr(user, "seller_profile") or not user.seller_profile.is_verified:
            return Response(
                {"error": "Not authorized or seller not approved."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=user.seller_profile)
        return Response({"success": True, "product": serializer.data}, status=status.HTTP_201_CREATED)


# ----------------------------
# Admin Login
# ----------------------------
class AdminLoginView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin_profile = serializer.validated_data["user"].admin_profile
        return Response({
            "message": "Admin login successful.",
            "admin": {
                "id": admin_profile.id,
                "full_name": admin_profile.full_name,
                "email": serializer.validated_data["user"].email,
            }
        }, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import SellerProfile
from .serializers import SellerSerializer, PublicSellerSerializer

class AdminSellerList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        sellers = SellerProfile.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)

class VerifySeller(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        seller = get_object_or_404(SellerProfile, pk=pk)
        action = request.data.get("action")  # "approve" or "reject"
        if action == "approve":
            seller.is_verified = True
        elif action == "reject":
            seller.is_verified = False
        seller.save()
        # Optional: create/send a notification object here
        return Response({"detail": f"Seller {action}d."}, status=status.HTTP_200_OK)


class PublicVerifiedSellersView(generics.ListAPIView):
    queryset = SellerProfile.objects.filter(is_verified=True)
    serializer_class = PublicSellerSerializer
    permission_classes = []  # no authentication required



from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AdminLoginSerializer

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response({
            "admin": {"id": data["user"].id, "username": data["user"].username},
            "token": data["access"]
        })





class SellerDetailByBusinessView(APIView):
    def get(self, request, name):
        try:
            seller = SellerProfile.objects.get(
                business_name__iexact=name.strip(), is_verified=True
            )
        except SellerProfile.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(SellerSerializer(seller).data, status=status.HTTP_200_OK)