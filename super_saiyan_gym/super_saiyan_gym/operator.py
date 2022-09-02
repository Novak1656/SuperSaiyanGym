from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from training_app.views import mailing, clean_training_process, reload_users_schedules


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', days=1, name='auto_mailing')
    def auto_mailing():
        mailing()

    @scheduler.scheduled_job('interval', days=1, name='auto_clean_training_process')
    def auto_clean_training_process():
        clean_training_process()

    @scheduler.scheduled_job('interval', weeks=1, name='auto_reload_users_schedules')
    def auto_reload_users_schedules():
        reload_users_schedules()

    scheduler.start()
