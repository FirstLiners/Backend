import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from stores.models import Store


class Command(BaseCommand):
    help = "Импорт сведений о торговых центрах из csv файла."

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "data",
                "st_df.csv",
            ),
            encoding="utf-8",
        ) as data:
            for line in csv.DictReader(data):
                if not Store.objects.filter(store_id=line["st_id"]).exists():
                    Store.objects.create(
                        store_id=line["st_id"],
                        city_id=line["st_city_id"],
                        division_code=line["st_division_code"],
                        type_format_id=int(line["st_type_format_id"]),
                        type_loc_id=int(line["st_type_loc_id"]),
                        type_size_id=int(line["st_type_size_id"]),
                        is_active=int(line["st_is_active"]),
                    )
