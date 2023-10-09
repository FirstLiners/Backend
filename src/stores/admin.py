from django.contrib import admin

from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    ordering = ["store_id"]
    search_fields = ["store_id"]
    list_display = ["store_id", "city_id", "is_active"]
    list_filter = [
        "type_format_id",
        "type_loc_id",
        "type_size_id",
        "is_active",
    ]
