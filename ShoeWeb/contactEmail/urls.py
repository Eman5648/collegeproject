from django.urls import path, reverse
from . import views 
from .views import Success, Contact

app_name = 'email'

urlpatterns = [
    path('contactform/', views.Contact, name='contactform'),
    path('success/', views.Success, name='success'),
]