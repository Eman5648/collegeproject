from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import product_list, product, single, new, confirm, delete

class TestUrls(SimpleTestCase):

    def test_product_list_url_is_resolves(self):
        url = reverse('products')
        self.assertEquals(resolve(url).func, product_list)

    def test_product_list_by_category_is_resolves(self):
        url = reverse('product_list_by_category', args=[1])
        self.assertEquals(resolve(url).func, product)

    def test_single_url_is_resolves(self):
        url = reverse('single', args=[1,'some-slug'])
        self.assertEquals(resolve(url).func, single)
    
    def test_new_url_is_resolves(self):
        url = reverse('new')
        self.assertEquals(resolve(url).func, new)

    def test_confirm_url_is_resolves(self):
        url = reverse('confirm')
        self.assertEquals(resolve(url).func, confirm)
    
    def test_delete_url_is_resolves(self):
        url = reverse('delete')
        self.assertEquals(resolve(url).func, delete)


