from django import forms
from django.contrib.auth import get_user_model

User = get_user_model
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ['first_name', 'last_name', 'email',"address", "address2", "city", "country", 
        'postal_code', "phone"]

       