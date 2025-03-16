from django.db import models
from store.models import product
from account.models import registration
# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

class Cart(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

