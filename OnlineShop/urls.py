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
from viewer.views import (BaseView, IndexView, TVDetailView, TVListView, TVCreateView, TVUpdateView, TVDeleteView,
                         FilteredTelevisionListView, ProfileView, SubmittableLoginView, CustomLogoutView, SubmittablePasswordChangeView)
from viewer.models import Television, Brand, TVOperationSystem, TVDisplayResolution, TVDisplayTechnology

admin.site.register([Television, Brand, TVDisplayResolution, TVDisplayTechnology, TVOperationSystem])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile_detail'),
    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('', BaseView.as_view(), name='home'),
    path('index', IndexView.as_view(), name='index'),
    path('tv/list', TVListView.as_view(), name='tv_list'),
    path('tv/create', TVCreateView.as_view(), name='tv_create'),
    path('tv/update/<pk>', TVUpdateView.as_view(), name='tv_update'),
    path('tv/delete/<pk>', TVDeleteView.as_view(), name='tv_delete'),
    path('tv/detail/<pk>', TVDetailView.as_view(), name='tv_detail'),
    path('tv/<str:smart_tv>/', FilteredTelevisionListView.as_view(), name='filtered_smart_tv'),
    path('tv/technology/<str:technology>/', FilteredTelevisionListView.as_view(), name='filtered_tv_by_technology'),
    path('tv/screen-size/<int:screen_size>/', FilteredTelevisionListView.as_view(), name='filtered_tv_by_screen_size'),
    path('tv/brand/<str:brand>/technology/<str:technology>/', FilteredTelevisionListView.as_view(),
         name='filtered_tv_by_brand_and_technology'),
]
