from django.shortcuts import render
from store.models import product

def index(request):
    pro = product.objects.all()
    return render(request,'index.html',{'pro':pro})

def about(request):
    return render(request,'about.html')