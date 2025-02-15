from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from home.models import Product
from .cart import Cart 
from .forms import CartAddProductForm
from django.conf import settings
from vouchers.forms import VoucherApplyForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
                        
    voucher_apply_form = VoucherApplyForm()     

    return render(request, 'cart.html',  dict(cart = cart,voucher_apply_form= voucher_apply_form))
