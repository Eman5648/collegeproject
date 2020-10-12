from django.urls import path
from . import views 


urlpatterns = [
        path('', views.product_list,
                name='products'),
        path('<int:category_id>/', views.product,
                name='product_list_by_category'),
        path('<int:id>/<slug:slug>/', views.single,
                name='single'),
        path('new/', views.new, name='new'),
        path('confirm/', views.confirm, name='confirm'),
        path('delete/', views.delete, name='delete'),
]