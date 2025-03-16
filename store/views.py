from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

from django.core.paginator import Paginator

def store(request, category_slug=None):
    if category_slug:
        pro = product.objects.filter(category__slug=category_slug, is_active=True)
    else:
        pro = product.objects.filter(is_active=True)

    price_filter = request.GET.getlist('price')
    if price_filter:
        q_objects = models.Q()
        for price in price_filter:
            if price == '0-100':
                q_objects |= models.Q(product_price__gte=0, product_price__lte=100)
            elif price == '100-200':
                q_objects |= models.Q(product_price__gte=100, product_price__lte=200)
            elif price == '200-300':
                q_objects |= models.Q(product_price__gte=200, product_price__lte=300)
            elif price == '300-400':
                q_objects |= models.Q(product_price__gte=300, product_price__lte=400)
            elif price == '400-500':
                q_objects |= models.Q(product_price__gte=400, product_price__lte=500)
        pro = pro.filter(q_objects)

    paginator = Paginator(pro, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'price_filter': price_filter,
    }

    return render(request, 'store/products.html', context)


def product_detail(request,category_slug,product_slug):

    single_product = product.objects.get(category__slug=category_slug,slug=product_slug)

    related_products = product.objects.filter(category=single_product.category).exclude(id=single_product.id)[:6]

    context = {
       'single_product':single_product, 
       'related_products':related_products,
    }
    return render(request,'store/product_detail.html',context)

@login_required(login_url='login')
def sell_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.seller = request.user
            product_instance.slug = slugify(product_instance.product_name)
            product_instance.save()
            return redirect('store')
    else:
        form = ProductForm()
    context = {
        'form':form,
    }
    return render(request,'store/sell.html',context)

def search(request):
    pro = []
    if 'search' in request.GET:

        keyword = request.GET['search']

        if keyword:
            pro = product.objects.filter(Q(product_name__icontains=keyword) | Q(product_detail__icontains=keyword))
        
    context = {
        'page_obj':pro,
    }
    return render(request,'store/products.html',context)

@login_required
def edit_product(request, product_id):
    print("Product ID:", product_id)
    Product = get_object_or_404(product, id=product_id, seller=request.user)  # Ensure only user's product

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=Product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('my_products')
    else:
        form = ProductForm(instance=Product)

    return render(request, 'product_edit.html', {'form': form, 'product': Product})


@login_required
def delete_product(request, product_id):
    Product = get_object_or_404(product, id=product_id, seller=request.user)
    Product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('my_products')
