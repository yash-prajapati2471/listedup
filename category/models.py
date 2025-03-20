from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = CloudinaryField('category_image')

    def __str__(self):
        return self.category_name
    
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])
