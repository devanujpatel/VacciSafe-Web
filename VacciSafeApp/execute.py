from apscheduler.schedulers.background import BackgroundScheduler
from VacciSafeApp import scheduler_jobs

scheduler = BackgroundScheduler()
scheduler.add_job(scheduler_jobs.reminder_emails, 'interval', seconds=10)
scheduler.start()
