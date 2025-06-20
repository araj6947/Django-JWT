"""inventoryapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import include,re_path as url
from django.urls import path
from django.contrib import admin
from rest_framework.routers import DefaultRouter

#Add your URLS in respective place.


from django.urls import path
from inventoryapp.views import (
    ProductListCreateView, ProductDeleteView,
    ProductUpdateView, ProductCategoryQueryView,
    ProductSortByPriceView,
)

urlpatterns = [

    # Inventory CRUD APIs
    path('inventory/items/', ProductListCreateView.as_view(), name='add_or_list_items'),
    path('inventory/items/<int:pk>/', ProductUpdateView.as_view(), name='edit_item'),
    path('inventory/items/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_item'),
    path('items/query/<str:category>/', ProductCategoryQueryView.as_view(), name='filter_by_category'),
    path('items/sort/', ProductSortByPriceView.as_view(), name='sort_by_price'),
]