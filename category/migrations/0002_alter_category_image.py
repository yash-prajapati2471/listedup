# Generated by Django 5.1.6 on 2025-03-20 04:57

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='category_image'),
        ),
    ]
