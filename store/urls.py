from django.urls import path
from .views import *

urlpatterns = [
    path('',store,name='store'),

    path('<category_slug>/',store,name='product_by_category'),

    path('<category_slug>/<product_slug>/',product_detail,name='product_detail'),

    path('search',search,name='search'),

    path('edit-product/<product_id>/',edit_product,name='edit_product'),

    path('delete-product/<product_id>/',delete_product,name='delete_product'),
]
