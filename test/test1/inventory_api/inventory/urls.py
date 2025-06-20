from django.urls import path
from .views import ItemListCreateView, ItemByCategory, ItemSortByPrice, ItemUpdateView


urlpatterns = [
    path('inventory/items/', ItemListCreateView.as_view()),                # GET, POST, DELETE
    path('inventory/items/<int:pk>/', ItemUpdateView.as_view()),          # PUT
    path('items/query/<str:category>/', ItemByCategory.as_view()),    # GET by category
    path('items/sort/', ItemSortByPrice.as_view()),                 # GET sorted by price desc
]