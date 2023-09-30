import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from skus.models import Category, Group, SKU, SubCategory


class Command(BaseCommand):
    help = 'Импорт сведений о товарной иерархии из csv файла.'

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "data",
                "pr_df.csv",
            ),
            encoding='utf-8'
        ) as data:
            for line in csv.DictReader(data):
                if not SKU.objects.filter(sku_id=line["pr_sku_id"]).exists():
                    if not Group.objects.filter(
                        group_id=line["pr_group_id"]
                    ).exists():
                        Group.objects.create(group_id=line["pr_group_id"])
                    if not Category.objects.filter(
                        cat_id=line["pr_cat_id"]
                    ).exists():
                        Category.objects.create(
                            cat_id=line["pr_cat_id"],
                            group=Group.objects.get(
                                group_id=line["pr_group_id"]
                            )
                        )
                    if not SubCategory.objects.filter(
                        subcat_id=line["pr_subcat_id"]
                    ).exists():
                        SubCategory.objects.create(
                            subcat_id=line["pr_subcat_id"],
                            category=Category.objects.get(
                                cat_id=line["pr_cat_id"]
                            )
                        )
                    SKU.objects.create(
                        sku_id=line["pr_sku_id"],
                        uom=line["pr_uom_id"],
                        subcategory=SubCategory.objects.get(
                            subcat_id=line["pr_subcat_id"]
                        ),
                    )
