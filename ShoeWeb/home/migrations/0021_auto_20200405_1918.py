# Generated by Django 3.0.3 on 2020-04-05 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_product_image2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
