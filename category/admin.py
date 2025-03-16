from django.contrib import admin
from .models import Category
# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ['category_name']
    prepopulated_fields = {'slug':('category_name',)}

admin.site.register(Category,AdminCategory)