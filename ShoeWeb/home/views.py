from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.db.models import Count
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from cart.forms import CartAddProductForm
from .forms import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

def product_list(request, category_id=None):
    category = None
    products = Product.objects.all()
    ccat = Category.objects.annotate(num_products=Count('products'))
    if(category_id):
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    return render(request, 'home.html', 
                            {'products':products, 
                            'countcat':ccat})
                            

def single(request, id,slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, "single.html",
                     {'product': product,
                     'cart_product_form': cart_product_form})

def product(request, category_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if(category_id):
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    return render(request, 'product.html', 
                            {'products':products, 
                            'categories': categories,
                            'category': category})

  

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form':form})

def signoutView(request):
    logout(request)
    return redirect('signin')




def search_result(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
    return render(request, 'search.html', {'query':query, 'products':products})

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def new(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=sub.email,
            subject='Newsletter Confirmation',
            html_content='Thank you for signing up for my email newsletter! \
                Please complete the process by \
                <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \
                confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'),
                                                    sub.email,
                                                    sub.conf_num))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return render(request, 'sub.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'sub.html', {'form': SubscriberForm()})

def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'sub.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'sub.html', {'email': sub.email, 'action': 'denied'})

def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'sub.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'sub.html', {'email': sub.email, 'action': 'denied'})