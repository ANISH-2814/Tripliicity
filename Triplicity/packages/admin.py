from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Package

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "description")

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "rating")
    list_filter = ("category",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
