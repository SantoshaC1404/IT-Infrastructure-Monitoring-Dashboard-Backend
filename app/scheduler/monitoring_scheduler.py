from apscheduler.schedulers.background import BackgroundScheduler

from app.db.session import SessionLocal
from app.services.monitoring.monitoring_service import MonitoringService

scheduler = BackgroundScheduler()


def run_monitoring_scheduler():

    db = SessionLocal()

    try:
        MonitoringService(db).monitor_all_devices()
    finally:
        db.close()


def start_monitoring_scheduler():

    scheduler.add_job(
        run_monitoring_scheduler,
        trigger="interval",
        seconds=120,
        # minutes=2,
        id="device_monitoring",
        replace_existing=True,
    )

    scheduler.start()
