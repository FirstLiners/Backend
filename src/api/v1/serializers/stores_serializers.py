from rest_framework import serializers

from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для торговых центров.
    """

    class Meta:
        model = Store
        fields = (
            "store_id",
            "city_id",
            "division_code",
            "type_format_id",
            "type_loc_id",
            "type_size_id",
            "is_active",
        )
