from rest_framework import serializers

from forecasts.models import Forecast


class ForecastSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода прогноз по продажам.
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
        )


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
