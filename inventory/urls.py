from django.urls import path
from . import views

from .views import create_product

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/add/', create_product, name='create_product'),
    path('products/<int:product_id>/<str:action>/', views.StockTransactionView.as_view(), name='stock_transaction'),
    path('chart/', views.inventory_chart, name='inventory_chart'),
     path('transactions/', views.transaction_report, name='transaction_report'),

]
