from rest_framework import serializers


from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для торговых центров.
    """

    class Meta:
        model = Store
        fields = ("store_id",)
