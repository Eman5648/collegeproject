from django.db import models
from django.urls import reverse
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Create your models here.
class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(null=True, unique=True)
    products = models.ManyToManyField('Product')
    image = models.ImageField(upload_to='imagess/', blank=True)
    def get_products(self):
        return Product.objects.filter(category=self)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=self.slug)

    

class Product(models.Model):
    name = models.TextField()
    slug = models.SlugField(null=True, unique=True)
    description = models.TextField()
    stock = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    image2 = models.ImageField(upload_to='images/', blank=True)
    image3 = models.ImageField(upload_to='images/', blank=True)
    image4 = models.ImageField(upload_to='images/', blank=True)
    image5 = models.ImageField(upload_to='images/', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('single',args=[self.id, self.slug])

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def size(self):
        return self.all().filter(category='size')
    
    def color(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
('size', 'size'),
('color', 'color'),
('package', 'package'),
)

class Variation(models.Model):
    product = models.ManyToManyField('Product')
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.title
        


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject=self.subject,
                    html_content=contents + (
                        '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri('/delete/'),
                            sub.email,
                            sub.conf_num))
            sg.send(message)