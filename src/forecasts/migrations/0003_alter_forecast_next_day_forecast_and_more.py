# Generated by Django 4.2.5 on 2023-10-07 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stores", "0001_initial"),
        ("skus", "0003_alter_subcategory_options"),
        ("forecasts", "0002_forecast_next_day_forecast_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forecast",
            name="next_day_forecast",
            field=models.PositiveIntegerField(
                verbose_name="Прогноз на следующий день"
            ),
        ),
        migrations.AlterField(
            model_name="forecast",
            name="next_day_real_sale",
            field=models.PositiveIntegerField(
                null=True, verbose_name="Реальные продажи на следующий день"
            ),
        ),
        migrations.CreateModel(
            name="StoreSKU",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Нужен прогноз"
                    ),
                ),
                (
                    "sku",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="stores",
                        to="skus.sku",
                        verbose_name="Товар",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="skus",
                        to="stores.store",
                        verbose_name="Торговый центр",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар магазина",
                "verbose_name_plural": "Товары магазинов",
                "ordering": ["store", "sku"],
            },
        ),
        migrations.AddConstraint(
            model_name="storesku",
            constraint=models.UniqueConstraint(
                fields=("store", "sku"), name="double store&sku (unique)"
            ),
        ),
        migrations.AlterIndexTogether(
            name="storesku",
            index_together={("store", "sku")},
        ),
    ]
