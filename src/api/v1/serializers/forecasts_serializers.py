from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from forecasts.models import Forecast, StoreSKU
from sales.models import Sale
from stores.models import Store
from skus.models import SKU


class ForecastSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода прогнозов.
    """

    store = serializers.CharField(source="store__store_id")
    group = serializers.CharField(
        source="sku__subcategory__category__group__group_id", read_only=True
    )
    category = serializers.CharField(
        source="sku__subcategory__category__cat_id", read_only=True
    )
    subcategory = serializers.CharField(
        source="sku__subcategory__subcat_id", read_only=True
    )
    sku = serializers.CharField(source="sku__sku_id")
    uom = serializers.CharField(source="sku__uom", read_only=True)

    class Meta:
        model = Forecast
        fields = (
            "store",
            "group",
            "category",
            "subcategory",
            "sku",
            "date",
            "forecast_data",
            "uom",
        )


class ForecastCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания прогнозов.
    """

    store = serializers.CharField()
    sku = serializers.CharField()

    class Meta:
        model = Forecast
        fields = (
            "store",
            "sku",
            "date",
            "forecast_data",
        )

    def create(self, validated_data):
        store_id = validated_data.pop("store")
        sku_id = validated_data.pop("sku")
        date = validated_data.pop("date")
        next_date = str((date + timedelta(days=1)))
        forecast_data = validated_data.pop("forecast_data")
        next_day_forecast = forecast_data[next_date]
        store = Store.objects.get(store_id=store_id)
        sku = SKU.objects.get(sku_id=sku_id)
        forecast = Forecast.objects.create(
            store=store,
            sku=sku,
            next_day_forecast=next_day_forecast,
            date=date,
            forecast_data=forecast_data,
            **validated_data,
        )
        if forecast.date < timezone.now().date():
            sales = Sale.objects.filter(
                sku=forecast.sku,
                store=forecast.store,
                date=forecast.date + timedelta(days=1),
            )
            if sales.exists():
                forecast.next_day_real_sale = sales.first().sales_in_units
                forecast.save()
        return forecast

    def validate(self, data):
        if not Store.objects.filter(store_id=data["store"]).exists():
            raise serializers.ValidationError(
                "Торговый центр с таким store_id не существует в системе."
            )
        if not SKU.objects.filter(sku_id=data["sku"]).exists():
            raise serializers.ValidationError(
                "Товар с таким sku_id не существует в системе."
            )
        if data["date"] > timezone.now().date():
            raise serializers.ValidationError(
                "Дата, на которую вводится прогоноз, позже текущей."
            )
        if Forecast.objects.filter(
            store__store_id=data["store"],
            sku__sku_id=data["sku"],
            date=data["date"],
        ).exists():
            raise serializers.ValidationError(
                (
                    "Прогноз для данного товара в данном "
                    "ТЦ на данную дату уже есть в системе."
                )
            )
        return data


class StatisticsListSerializer(serializers.ListSerializer):
    """
    Сериализатор для вывода статистики по прогнозам,
    объединенной по паре товар - магазин.
    Пока не требуется :(
    """

    def to_representation(self, data):
        statistic = []
        for forecast in range(0, len(data)):
            info = {
                "store": data[forecast]["store__store_id"],
                "sku": data[forecast]["sku__sku_id"],
                "data": [
                    {
                        "real_sale": data[forecast]["real_sale"],
                        "forecast": data[forecast]["forecast"],
                        "period": data[forecast]["period"],
                    }
                ],
            }
            if forecast == 0:
                statistic.append(info)
            else:
                if (
                    statistic[-1]["store"] == data[forecast]["store__store_id"]
                    and statistic[-1]["sku"] == data[forecast]["sku__sku_id"]
                ):
                    statistic[-1]["data"].append(
                        {
                            "real_sale": data[forecast]["real_sale"],
                            "forecast": data[forecast]["forecast"],
                            "period": data[forecast]["period"],
                        }
                    )
                else:
                    statistic.append(info)
        return statistic


class StatisticsSerializer(serializers.Serializer):
    """
    Сериализатор для вывода статистики по прогнозам.
    """

    store = serializers.CharField(source="store__store_id", read_only=True)
    group = serializers.CharField(
        source="sku__subcategory__category__group__group_id", read_only=True
    )
    category = serializers.CharField(
        source="sku__subcategory__category__cat_id", read_only=True
    )
    subcategory = serializers.CharField(
        source="sku__subcategory__subcat_id", read_only=True
    )
    sku = serializers.CharField(source="sku__sku_id", read_only=True)
    uom = serializers.CharField(source="sku__uom", read_only=True)
    real_sale = serializers.IntegerField(read_only=True)
    forecast = serializers.IntegerField(read_only=True)
    difference = serializers.IntegerField(read_only=True)
    period = serializers.IntegerField(read_only=True)
    wape = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            "store",
            "group",
            "category",
            "subcategory",
            "sku",
            "real_sale",
            "forecast",
            "period",
            "difference",
            "wape",
        )


class StoreSKUSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пар товар/магазин, по которым нужен прогноз.
    """

    store = serializers.StringRelatedField(read_only=True)
    sku = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StoreSKU
        fields = ["store", "sku"]
