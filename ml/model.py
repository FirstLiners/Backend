from typing import List

import os
import pandas as pd
import pickle


data = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "set_for_prediction.csv")
)

# выбираем магазин и товар
data2 = data[
    (data["st_id_key"] == "084a8a9aa8cced9175bd07bc44998e75")
    & (data["pr_sku_id_key"] == "0376a60d9a7ce7965beddc4815588697")
]

# убираем ненужные колонки
data2 = data2.drop(["date", "date.1", "st_id_key", "pr_sku_id_key"], axis=1)


# загружаем модель
loaded_model = pickle.load(
    open(os.path.join(os.path.dirname(__file__), "finalized_model.sav"), "rb")
)
print(data2)
# делаем предсказания
predictions = loaded_model.predict(data2)
print(predictions)


def forecast(store_id: str, sku_id: str) -> List[int]:
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "set_for_prediction.csv")
    )

    data2 = data[
        (data["st_id_key"] == store_id) & (data["pr_sku_id_key"] == sku_id)
    ]

    data2 = data2.drop(
        ["date", "date.1", "st_id_key", "pr_sku_id_key"], axis=1
    )

    loaded_model = pickle.load(
        open(
            os.path.join(os.path.dirname(__file__), "finalized_model.sav"),
            "rb",
        )
    )

    return loaded_model.predict(data2)
