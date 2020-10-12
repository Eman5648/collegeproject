from django.test import SimpleTestCase
from django.urls import reverse, resolve
from contactEmail.views import Contact, Success

class TestUrls(SimpleTestCase):

    def test_contact_form_url_is_resolves(self):
        url = reverse('email:contactform')
        self.assertEquals(resolve(url).func, Contact)

    def test_success_url_is_resolves(self):
        url = reverse('email:success')
        self.assertEquals(resolve(url).func, Success)