"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('defaultadmindjangopage/', admin.site.urls),
    path('', views.home, name='home'),
    path('admindashboard/', views.admindashboard, name="admindashboard"),
    # path('verification/', views.email_verification, name="verification"),
    # path('verify-code/', views.verify_code, name="verify_code"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    path('shop/', views.shop, name="shop"),
    path('shop/category/<str:category_name>/', views.shop_by_category, name='shop_by_category'),
    path('aboutus/', views.about, name="about"),
    path('contactus/', views.contact, name="contact"),
    path('blog/', views.blog, name="blog"),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('addcategories/', views.addcategories, name="addcategories"),
    path('viewcategories/', views.viewcategories, name="viewcategories"),
    path('addproduct/', views.addproduct, name="addproduct"),
    path('viewproducts/', views.viewproducts, name="viewproducts"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
