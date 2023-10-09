from celery import Celery
from ml_app import main
from celery.schedules import crontab


app = Celery("forecast", broker="redis://localhost:6379/0")


@app.task
def make_forecast():
    main()


app.conf.beat_schedule = {
    "make_forecast_every_night": {
        "task": "make_forecast",
        "schedul": crontab(hour=1, minute=16),
    }
}
