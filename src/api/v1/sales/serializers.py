from rest_framework import serializers

from sales.models import Sale


class SaleGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения данных по продажам.
    """

    sku_id = serializers.CharField(source="sku.sku_id")
    store_id = serializers.CharField(source="store.store_id")

    class Meta:
        model = Sale
        fields = (
            "store_id",
            "sku_id",
            "date",
            "sales_type_id",
            "sales_in_units",
            "promo_sales_in_units",
            "sales_in_rub",
            "promo_sales_in_rub",
        )
