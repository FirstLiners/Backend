from django.contrib import admin

from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    search_fields = ["store__store_id", "sku__sku_id", "date"]
    list_display = ["store", "sku", "date"]
