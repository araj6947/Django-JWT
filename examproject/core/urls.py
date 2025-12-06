
from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('list/gadgets/',GadgetListView.as_view(),name='my-gadgets'),
    path('list/admin/',AdminListView.as_view(),name='admin-list')
]
