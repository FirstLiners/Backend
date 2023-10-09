import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from forecasts.models import StoreSKU
from stores.models import Store
from skus.models import SKU


class Command(BaseCommand):
    help = "Импорт пар товар магазин, по котоым нужен прогноз, из csv файла."

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "data",
                "sales_df_train.csv",
            ),
            encoding="utf-8",
        ) as data:
            for line in csv.DictReader(data):
                if not StoreSKU.objects.filter(
                    store__store_id=line["st_id"],
                    sku__sku_id=line["pr_sku_id"],
                ).exists():
                    StoreSKU.objects.create(
                        store=Store.objects.get(store_id=line["st_id"]),
                        sku=SKU.objects.get(sku_id=line["pr_sku_id"]),
                    )
