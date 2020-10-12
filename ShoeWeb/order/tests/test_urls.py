from django.test import SimpleTestCase
from django.urls import reverse, resolve
from order.views import order_create, order_history, cancel_order

class TestUrls(SimpleTestCase):

    def test_order_create_url_is_resolves(self):
        url = reverse('order_create')
        self.assertEquals(resolve(url).func, order_create)

    def test_order_history_url_is_resolves(self):
        url = reverse('order_history')
        self.assertEquals(resolve(url).func, order_history)

    def test_order_cancel_url_is_resolves(self):
        url = reverse('cancel_order', args=[1])
        self.assertEquals(resolve(url).func, cancel_order)