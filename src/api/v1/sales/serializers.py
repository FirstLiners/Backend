from django.utils import timezone
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

    def validate(self, data):
        if not Store.objects.filter(store_id=data["store_id"]).exists():
            raise serializers.ValidationError(
                "Торговый центр с таким store_id не существует в системе."
            )
        if not SKU.objects.filter(sku_id=data["sku_id"]).exists():
            raise serializers.ValidationError(
                "Товар с таким sku_id не существует в системе."
            )
        if data["date"] > timezone.now().date():
            raise serializers.ValidationError(
                "Дата, на которую вводится продажа, позже текущей."
            )
        if Sale.objects.filter(
            store__store_id=data["store_id"],
            sku__sku_id=data["sku_id"],
            date=data["date"],
        ).exists():
            raise serializers.ValidationError(
                (
                    "Информация о продаже данного товара в данном "
                    "ТЦ на данную дату уже есть в системе."
                )
            )
        return data
