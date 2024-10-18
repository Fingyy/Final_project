"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from viewer.views import (BaseView, TVDetailView, TVListView, TVCreateView, TVUpdateView, TVDeleteView,
                          FilteredTelevisionListView, ProfileView, SubmittableLoginView, CustomLogoutView,
                          SubmittablePasswordChangeView, MobileListView, CreateOrderView, OrderSuccessView,
                          OrderListView, OrderDetailView, AddToCartView, RemoveFromCartView, CartView, CheckoutView,
                          edit_profile, signup, BrandCreateView, SearchResultsView, ItemOnStockListView,
                          ItemOnStockCreateView, ItemOnStockUpdateView, ItemOnStockDeleteView)
from viewer.models import (Profile, Television, Brand, TVOperationSystem, TVDisplayResolution, TVDisplayTechnology,
                           MobilePhone, MobileDisplay, MobileConstruction, MobileUserMemory, MobileRAM,
                           MobileOperationSystem, Order, ItemsOnStock
                           )

from django.conf import settings
from django.conf.urls.static import static

admin.site.register([Television, Brand, TVDisplayResolution, TVDisplayTechnology, TVOperationSystem, MobilePhone,
                     MobileDisplay, MobileConstruction, MobileUserMemory, MobileRAM, MobileOperationSystem, Profile,
                     Order, ItemsOnStock])

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    # ----------------Profil sekce----------------
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', ProfileView.as_view(), name='profile_detail'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    # ----------------TV sekce----------------
    path('brand/create/', BrandCreateView.as_view(), name='brand_create'),
    path('tv/list/', TVListView.as_view(), name='tv_list'),
    path('tv/create/', TVCreateView.as_view(), name='tv_create'),
    path('tv/update/<pk>', TVUpdateView.as_view(), name='tv_update'),
    path('tv/delete/<pk>', TVDeleteView.as_view(), name='tv_delete'),
    path('tv/<pk>', TVDetailView.as_view(), name='tv_detail'),
    path('tv/detail/<str:smart_tv>/', FilteredTelevisionListView.as_view(), name='filtered_smart_tv'),
    path('tv/technology/<str:technology>/', FilteredTelevisionListView.as_view(), name='filtered_tv_by_technology'),
    path('tv/resolution/<str:resolution>/', FilteredTelevisionListView.as_view(), name='filtered_tv_by_resolution'),
    path('tv/oper-system/<str:op_system>/', FilteredTelevisionListView.as_view(), name='filtered_tv_by_op_system'),
    path('tv/brand/<str:brand>/technology/<str:technology>/', FilteredTelevisionListView.as_view(),
         name='filtered_tv_by_brand_and_technology'),
    # ----------------Mobil sekce----------------
    path('mobile', MobileListView.as_view(), name='mobile_list'),
    # ----------------Sklad sekce----------------
    path('stock', ItemOnStockListView.as_view(), name='stock_list'),
    path('stock/create/', ItemOnStockCreateView.as_view(), name='item_on_stock_create'),
    path('stock/update/<pk>', ItemOnStockUpdateView.as_view(), name='item_on_stock_update'),
    path('stock/delete/<pk>', ItemOnStockDeleteView.as_view(), name='item_on_stock_delete'),
    # ----------------Cart & Order sekce----------------
    path('cart/add/<int:television_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:television_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/create/<int:television_id>/', CreateOrderView.as_view(), name='create_order'),
    path('order/success/<uuid:order_id>/', OrderSuccessView.as_view(), name='order_success'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/<uuid:order_id>/', OrderDetailView.as_view(), name='order_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
