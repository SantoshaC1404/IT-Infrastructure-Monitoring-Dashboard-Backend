from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.scheduler.jobs import collect_metrics_job

scheduler = BackgroundScheduler(timezone="UTC")


def start_scheduler():

    scheduler.add_job(
        collect_metrics_job,
        trigger=IntervalTrigger(minutes=1),
        id="monitoring-job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()


def stop_scheduler():

    scheduler.shutdown(wait=False)
