from django.urls import path
from .views import *
from store.views import sell_product
from olx_project.views import about

urlpatterns = [
    path('chat/<product_id>/',chat_with_seller,name='chat_with_seller'),
    path('chat-room/<room_id>/',chat_room,name='chat_room'),
    path('chat-list/',chat_list,name='chat_list'),
    path('sell/',sell_product,name='sell_product'),
    path('get-messages/<room_id>/',get_messages,name='get_messages'),
    path('about/',about,name='about'),
]
