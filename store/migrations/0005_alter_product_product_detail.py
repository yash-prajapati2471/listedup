# Generated by Django 5.1.6 on 2025-03-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_detail',
            field=models.TextField(),
        ),
    ]
