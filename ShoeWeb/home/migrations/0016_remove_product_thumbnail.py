# Generated by Django 3.0.3 on 2020-03-31 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_product_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
    ]
