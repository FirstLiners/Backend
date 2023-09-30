from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from skus.models import Group, Category, SKU, SubCategory
from stores.models import Store

User = get_user_model()


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(
            email="vasya@vasya.ru",
            password="vasya123",
        )
        cls.user.set_password("vasya123")
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


class TestStoreFixture(TestUserFixture):
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
