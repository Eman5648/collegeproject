# Generated by Django 2.2 on 2020-02-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='imagess/'),
        ),
    ]
