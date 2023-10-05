from io import BytesIO
from tempfile import NamedTemporaryFile
import openpyxl


def forecast_file_creation(forecasts):
    """
    Создание файла с актуальными прогнозами в формате xls.
    """

    file = openpyxl.Workbook()
    active_list = file.active
    active_list.title = "Актуальный прогноз"
    column_titles = [
        "ТК",
        "Группа товара",
        "Категория товара",
        "Подкатегория товара",
        "Товар",
    ]
    for i in range(1, 15):
        column_titles.append(f"День{i}")
    active_list.append(column_titles)
    for forecast in forecasts:
        data = [
            forecast["store__store_id"],
            forecast["sku__subcategory__category__group__group_id"],
            forecast["sku__subcategory__category__cat_id"],
            forecast["sku__subcategory__subcat_id"],
            forecast["sku__sku_id"],
        ]
        for k, v in forecast["forecast_data"].items():
            data.append(v)
        active_list.append(data)
    with NamedTemporaryFile() as tmp:
        file.save(tmp.name)
        output = BytesIO(tmp.read())
        return output


def statistics_file_creation(statistics):
    """
    Создание файла со статистикой по прогнозам в формате xlsx.
    """

    file = openpyxl.Workbook()
    active_list = file.active
    active_list.title = "Статистика по прогнозам"
    column_titles = [
        "ТК",
        "Группа товара",
        "Категория товара",
        "Подкатегория товара",
        "Товар",
        "Ед.измерения",
        "Период",
        "Продажи факт",
        "Продажи прогноз",
        "Разница факт/план",
        "Качество прогноза по WAPE",
    ]
    active_list.append(column_titles)
    for stat in statistics:
        data = [
            stat["store__store_id"],
            stat["sku__sku_id"],
            stat["sku__subcategory__category__cat_id"],
            stat["sku__subcategory__subcat_id"],
            stat["sku__sku_id"],
            stat["sku__uom"],
            stat["period"],
            stat["real_sale"],
            stat["forecast"],
            stat["difference"],
            stat["wape"],
        ]
        active_list.append(data)
    with NamedTemporaryFile() as tmp:
        file.save(tmp.name)
        output = BytesIO(tmp.read())
        return output
