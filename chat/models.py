from django.db import models
from account.models import registration
from django.contrib.auth.models import User
from store.models import product as Product
# Create your models here.

class ChatRoom(models.Model):
    buyer = models.ForeignKey(registration,on_delete=models.CASCADE,related_name='buyer_chats')
    seller = models.ForeignKey(registration,on_delete=models.CASCADE,related_name='seller_chats')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom between {self.buyer} and {self.seller} for {self.product.product_name}"
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(registration,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
    

