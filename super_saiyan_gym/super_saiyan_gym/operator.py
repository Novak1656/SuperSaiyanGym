from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from training_app.views import mailing


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', days=1, name='auto_mailing')
    def auto_mailing():
        mailing()

    scheduler.start()
