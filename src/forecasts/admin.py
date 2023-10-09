from django.contrib import admin

from .models import Forecast, StoreSKU


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    search_fields = ["store__store_id", "sku__sku_id", "date"]
    list_display = ["store", "sku", "date"]


@admin.register(StoreSKU)
class StoreSKUAdmin(admin.ModelAdmin):
    search_fields = ["store__store_id", "sku__sku_id",]
    list_display = ["store", "sku",]
