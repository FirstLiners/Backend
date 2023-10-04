from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from forecasts.models import Forecast
from .models import Sale


@receiver(post_save, sender=Sale)
def forecast_real_sales_filling(sender, instance, created, **kwargs):
    """
    Заполнение информации о реальных продажах
    для прогноза предыдущего дня.
    """

    if created:
        forecast = Forecast.objects.filter(
            sku=instance.sku,
            store=instance.store,
            date=instance.date - timedelta(days=1)
        ).first()
        if forecast.exists():
            forecast.next_day_real_sale = instance.sales_in_units
