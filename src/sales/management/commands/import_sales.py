import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from sales.models import Sale
from stores.models import Store
from skus.models import SKU


class Command(BaseCommand):
    help = 'Импорт исторических сведений о продажах из csv файла.'

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "data",
                "sales_df_train.csv",
            ),
            encoding='utf-8'
        ) as data:
            for line in csv.DictReader(data):
                if not Sale.objects.filter(
                    store__store_id=line["st_id"],
                    sku__sku_id=line["pr_sku_id"],
                    date=line["date"],
                ).exists():
                    Sale.objects.create(
                        store=Store.objects.get(store_id=line["st_id"]),
                        sku=SKU.objects.get(sku_id=line["pr_sku_id"]),
                        date=line["date"],
                        sales_type_id=line["pr_sales_type_id"],
                        sales_in_units=line["pr_sales_in_units"],
                        promo_sales_in_units=line["pr_promo_sales_in_units"],
                        sales_in_rub=line["pr_sales_in_rub"],
                        promo_sales_in_rub=line["pr_promo_sales_in_rub"],
                    )
