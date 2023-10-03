from rest_framework import serializers

from sales.models import Sale
from skus.models import SKU
from stores.models import Store


class SaleSerializer(serializers.ModelSerializer):
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


class SaleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки данных о продажах.
    """

    sku_id = serializers.CharField()
    store_id = serializers.CharField()

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

    def create(self, validated_data):
        store_id = validated_data.pop("store_id")
        sku_id = validated_data.pop("sku_id")
        store = Store.objects.get(store_id=store_id)
        sku = SKU.objects.get(sku_id=sku_id)
        sale = Sale.objects.create(store=store, sku=sku, **validated_data)
        return sale
