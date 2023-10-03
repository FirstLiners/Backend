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
            tmp.seek(0)
            stream = tmp.read()
    return stream