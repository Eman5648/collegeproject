from django.shortcuts import render,redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart 
from home.models import Product
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import stripe
from datetime import datetime, timezone
from django.contrib import messages

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.voucher:
                order.voucher = cart.voucher
                order.discount = cart.voucher.discount
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            
            cart.clear()
            return render(request,
                            'created.html',
                            {'order': order})
    else:
        form = OrderCreateForm()

    stripe_total = cart.get_total_price_after_discount() * 100 
    description = 'Online Shop - New Order'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    return render(request,
                    'address.html',
                    dict(cart= cart, form=form,data_key = data_key, stripe_total=stripe_total , description = description))



@login_required()
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(email=email)
        paginator = Paginator(order_details, 3)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            orders = paginator.page(page)
        except (EmptyPage, InvalidPage):
            orders = paginator.page(paginator.num_pages)
    return render(request, 'order.html', {'order_details':order_details})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created
    current_date = datetime.now(timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    if minutes_diff <= 30:
        order.delete()
        messages.add_message(request, messages.INFO, 
        'Order is now cancelled')
    else:
        messages.add_message(request, messages.INFO,
         'Sorry, it is too late to cancel this order')
    return redirect('order_history')