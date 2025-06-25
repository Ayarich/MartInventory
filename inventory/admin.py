from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Supplier, Product, StockTransaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email']
    search_fields = ['name', 'contact_person']
    list_filter = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'supplier', 'buying_price', 'selling_price', 'quantity_in_stock', 'reorder_level']
    list_filter = ['category', 'supplier']
    search_fields = ['name']
    list_editable = ['quantity_in_stock', 'reorder_level']

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'date']
    list_filter = ['transaction_type', 'product']
    search_fields = ['product__name']
