from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, StockTransaction
from django.views import View
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'search_query': query
    })


from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Product, StockTransaction

class StockTransactionView(View):
    def post(self, request, product_id, action):
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity <= 0:
                messages.error(request, 'Please enter a positive quantity.')
                return redirect('product_list')
        except (TypeError, ValueError):
            messages.error(request, 'Invalid quantity.')
            return redirect('product_list')

        if action == 'in':
            product.quantity_in_stock += quantity
            transaction_type = 'IN'
        elif action == 'out':
            if quantity > product.quantity_in_stock:
                messages.error(request, 'Not enough stock to complete transaction.')
                return redirect('product_list')
            product.quantity_in_stock -= quantity
            transaction_type = 'OUT'
        else:
            messages.error(request, 'Invalid action.')
            return redirect('product_list')

        product.save()

        StockTransaction.objects.create(
            product=product,
            transaction_type=transaction_type,
            quantity=quantity,
            date=timezone.now()
        )

        messages.success(request, f'Successfully recorded stock {transaction_type.lower()} for {product.name}.')
        return redirect('product_list')




from .forms import ProductForm
from django.urls import reverse_lazy

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/create_product.html', {'form': form})






def transaction_report(request):
    transactions = StockTransaction.objects.select_related('product').order_by('-date')
    query = request.GET.get('q', '')
    if query:
        transactions = transactions.filter(product__name__icontains=query)
    return render(request, 'inventory/transaction_report.html', {
        'transactions': transactions,
        'query': query
    })


def inventory_chart(request):
    recent_transactions = StockTransaction.objects.filter(
        date__gte=timezone.now() - timedelta(days=30)
    )

    products = Product.objects.all()
    labels = []
    stock_in_data = []
    stock_out_data = []

    for product in products:
        labels.append(product.name)
        stock_in = recent_transactions.filter(product=product, transaction_type='IN').aggregate(total=Sum('quantity'))['total'] or 0
        stock_out = recent_transactions.filter(product=product, transaction_type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
        stock_in_data.append(stock_in)
        stock_out_data.append(stock_out)

    return render(request, 'inventory/inventory_chart.html', {
        'labels': labels,
        'stock_in_data': stock_in_data,
        'stock_out_data': stock_out_data
    })


# inventory/views.py
def transaction_report(request):
    transactions = StockTransaction.objects.select_related('product').order_by('-date')

    query = request.GET.get('q', '')
    if query:
        transactions = transactions.filter(product__name__icontains=query)

    return render(request, 'inventory/transaction_report.html', {
        'transactions': transactions,
        'query': query
    })