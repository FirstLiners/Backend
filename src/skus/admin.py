from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Group, Category, SubCategory, SKU


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    ordering = ["group_id"]
    search_fields = ["group_id"]
    list_display = ["group_id"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    ordering = ["cat_id"]
    search_fields = ["cat_id"]
    list_display = ["cat_id"]


@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    ordering = ["subcat_id"]
    search_fields = ["subcat_id"]
    list_display = ["subcat_id"]


@admin.register(SKU)
class SKUAdmin(ModelAdmin):
    ordering = ["sku_id"]
    search_fields = ["sku_id"]
    list_display = ["sku_id", "uom"]
    list_filter = ["uom"]
