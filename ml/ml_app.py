import logging
import os
import requests

from datetime import date
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


URL_STORES_SALES = "api/v1/forecast_data/"
URL_FORECAST = "api/v1/load_forecasts/"
URL_TOKEN = "api/v1/users/token/"

api_port = os.getenv("API_PORT")
api_host = os.getenv("API_HOST")
ml_user_email = os.getenv("ML_USER_EMAIL")
ml_user_password = os.getenv("ML_USER_PASSWORD")

_logger = logging.getLogger(__name__)


def setup_logging():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s"
    )
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m)


def get_address(resource):
    return "http://" + api_host + ":" + api_port + "/" + resource


def get_token():
    token_url = get_address(URL_TOKEN)
    access_data = {
        "email": ml_user_email,
        "password": ml_user_password,
    }
    response = requests.post(token_url, json=access_data)
    _logger.info(response.status_code)

    return requests.post(token_url, json=access_data).json()["access"]


def get_stores_skus():
    token = get_token()
    stores_skus_url = get_address(URL_STORES_SALES)
    resp = requests.get(
        stores_skus_url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=3,
    )
    if resp.status_code != 200:
        _logger.warning("Could not get stores list")
        return []
    return resp.json()


def main(today=date.today()):
    stores_skus = get_stores_skus()
    result = []
    # Здесь вызывается функция прогноза
    for i in stores_skus:
        data = {
            "store": i["store"],
            "sku": i["sku"],
            "date": str(today),
            "forecast_data": {
                "2023-10-09": 1,
                "2023-10-04": 3,
                "2023-10-05": 7,
                "2023-10-06": 9,
                "2023-10-07": 0,
                "2023-10-08": 1,
                "2023-10-16": 3,
                "2023-10-10": 7,
                "2023-10-11": 9,
                "2023-10-12": 0,
                "2023-10-13": 1,
                "2023-10-14": 1,
                "2023-10-15": 3,
            },
        }
        result.append(data)
    token = get_token()
    requests.post(
        get_address(URL_FORECAST),
        json=result,
        headers={"Authorization": f"Bearer {token}"},
    )


if __name__ == "__main__":
    setup_logging()
    main()
