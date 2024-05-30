from django.urls import path
from . import views

urlpatterns = [
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]
