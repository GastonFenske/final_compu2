from celery import Celery

celery = Celery('main_app')

celery.conf.update(
    broker_url = 'redis://192.168.0.124:6379/0',
    result_backend ='redis://192.168.0.124:6379/0',
    imports = (
        'tasks'
    )
)