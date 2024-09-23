from datetime import timedelta

from django.db.models import Max
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from forecasts.models import Forecast
from skus.models import Group, Category, SKU, SubCategory
from stores.models import Store
from sales.models import Sale

User = get_user_model()


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(
            email="user123@user.ru",
            password="user123",
        )
        cls.user.set_password("user123")
        cls.user.save()
        cls.user_client = APIClient()
        cls.user_client.force_authenticate(cls.user)
        cls.anon_client = APIClient()


class TestSKUFixture(TestUserFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group1 = Group.objects.create(group_id="group1_id")
        cls.group2 = Group.objects.create(group_id="group2_id")
        cls.cat11 = Category.objects.create(
            cat_id="cat11_id",
            group=cls.group1,
        )
        cls.cat12 = Category.objects.create(
            cat_id="cat12_id",
            group=cls.group1,
        )
        cls.cat21 = Category.objects.create(
            cat_id="cat21_id",
            group=cls.group1,
        )
        cls.cat22 = Category.objects.create(
            cat_id="cat22_id",
            group=cls.group1,
        )
        cls.subcat111 = SubCategory.objects.create(
            subcat_id="subcat111_id",
            category=cls.cat11,
        )
        cls.subcat112 = SubCategory.objects.create(
            subcat_id="subcat112_id",
            category=cls.cat11,
        )
        cls.subcat121 = SubCategory.objects.create(
            subcat_id="subcat121_id",
            category=cls.cat12,
        )
        cls.subcat211 = SubCategory.objects.create(
            subcat_id="subcat211_id",
            category=cls.cat21,
        )
        cls.subcat221 = SubCategory.objects.create(
            subcat_id="subcat221_id",
            category=cls.cat22,
        )
        cls.subcat222 = SubCategory.objects.create(
            subcat_id="subcat222_id",
            category=cls.cat22,
        )
        cls.sku1 = SKU.objects.create(
            sku_id="sku1_id",
            uom=1,
            subcategory=cls.subcat111,
        )
        cls.sku2 = SKU.objects.create(
            sku_id="sku2_id",
            uom=2,
            subcategory=cls.subcat112,
        )
        cls.sku3 = SKU.objects.create(
            sku_id="sku3_id",
            uom=1,
            subcategory=cls.subcat121,
        )
        cls.sku4 = SKU.objects.create(
            sku_id="sku4_id",
            uom=3,
            subcategory=cls.subcat211,
        )
        cls.sku5 = SKU.objects.create(
            sku_id="sku5_id",
            uom=2,
            subcategory=cls.subcat221,
        )
        cls.sku6 = SKU.objects.create(
            sku_id="sku6_id",
            uom=1,
            subcategory=cls.subcat222,
        )
        cls.sku7 = SKU.objects.create(
            sku_id="sku7_id",
            uom=1,
            subcategory=cls.subcat222,
        )


class TestStoreFixture(TestSKUFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.store1 = Store.objects.create(
            store_id="store1_id",
            city_id="city1_id",
            division_code="division_1",
            type_format_id=1,
            type_loc_id=3,
            type_size_id=3,
            is_active=1,
        )
        cls.store2 = Store.objects.create(
            store_id="store2_id",
            city_id="city1_id",
            division_code="division_2",
            type_format_id=2,
            type_loc_id=4,
            type_size_id=3,
            is_active=1,
        )


class TestSalesFixture(TestStoreFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale1 = Sale.objects.create(
            store=cls.store1,
            sku=cls.sku1,
            date=timezone.now().date(),
            sales_type_id=1,
            sales_in_units=1.000,
            promo_sales_in_units=1.000,
            sales_in_rub=103.00,
            promo_sales_in_rub=103.00,
        )
        cls.sale2 = Sale.objects.create(
            store=cls.store2,
            sku=cls.sku2,
            date=timezone.now().date(),
            sales_type_id=1,
            sales_in_units=3.000,
            promo_sales_in_units=3.000,
            sales_in_rub=703.00,
            promo_sales_in_rub=703.00,
        )


class TestForecastsFixture(TestSalesFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.frcst_query = Forecast.objects.values(
            "store__store_id",
            "sku__sku_id",
            "sku__subcategory__subcat_id",
            "sku__subcategory__category__cat_id",
            "sku__subcategory__category__group__group_id",
            "sku__uom",
            "forecast_data",
        ).annotate(date=Max("date"))
        data = {}
        for i in range(1, 15):
            data[str(timezone.now().date() + timedelta(days=i))] = i

        cls.forecast1 = Forecast.objects.create(
            store=cls.store1,
            sku=cls.sku1,
            date=timezone.now().date(),
            forecast_data=data,
            next_day_forecast=1,
        )
        cls.forecast2 = Forecast.objects.create(
            store=cls.store2,
            sku=cls.sku2,
            date=timezone.now().date(),
            forecast_data=data,
            next_day_forecast=1,
        )
