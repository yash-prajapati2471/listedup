from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',registration,name='registration'),
    path('verification/<uid64>/<token>/',verification,name='verification'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('contact/',Contact,name='Contact'),
    path('my-products/', my_products, name='my_products'),
    path('profile/',profile,name='profile'),
    path('change_password/',change_password,name='change_password'),
]
