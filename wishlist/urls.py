from django.urls import path
from .views import *

urlpatterns = [
    path('',wishlist, name='wishlist'), 
    path('add/<product_id>/',add_to_wishlist, name='add_to_wishlist'), 
    path('remove/<product_id>/',remove_from_wishlist, name='remove_from_wishlist'),
    path('faqs/',faqs,name='faqs'),
]
