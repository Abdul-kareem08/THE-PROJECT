from django.urls import path
from .views import (
    home,
    SellerRegisterView,
    SellerLoginView,
    PendingSellersView,
    VerifiedSellersView,
    ApproveSellerView,
    SellerNotificationsView,
    AdminLoginView,
    ProductUploadView,
    PublicVerifiedSellersView,
    AdminSellerList,
    VerifySeller, 
    AdminLoginView,
    SellerDetailByBusinessView,
)

urlpatterns = [
    # Root
    path("", home, name="home"),

    # ----------------------------
    # Seller Endpoints
    # ----------------------------
    path("sellers/register/", SellerRegisterView.as_view(), name="seller-register"),
    path("sellers/login/", SellerLoginView.as_view(), name="seller-login"),
    path("sellers/pending/", PendingSellersView.as_view(), name="pending-sellers"),
    path("sellers/verified/", VerifiedSellersView.as_view(), name="verified-sellers"),
    path("sellers/<int:id>/approve/", ApproveSellerView.as_view(), name="approve-seller"),
    path("sellers/notifications/", SellerNotificationsView.as_view(), name="seller-notifications"),
    path("products/upload/", ProductUploadView.as_view(), name="product-upload"),
    path("sellers/by-business/<str:name>/", SellerDetailByBusinessView.as_view(),
         name="seller-by-business"),

    # ----------------------------
    # Admin Endpoints
    # ----------------------------
    path("admins/login/", AdminLoginView.as_view(), name="admin-login"),
    path("sellers/verified/public/", PublicVerifiedSellersView.as_view(), name="public-verified-sellers"),
    path("admins/login/", AdminLoginView.as_view(), name="admin-login"),
    path("admins/sellers/", AdminSellerList.as_view(), name="admin-seller-list"),
    path("admins/sellers/<int:pk>/verify/", VerifySeller.as_view(), name="verify-seller"),
]
