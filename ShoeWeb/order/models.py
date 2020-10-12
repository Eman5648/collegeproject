from django.db import models
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from vouchers.models import Voucher
from decimal import Decimal


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120,null=True)
    country = models.CharField(max_length=120, )
    postal_code = models.CharField(max_length=20)
    phone =models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    voucher = models.ForeignKey(Voucher,
                                related_name='orders',
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0),
                                    MaxValueValidator(100)])

   
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                            on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity