from celery import Celery
# import sys
# sys.path.append('.')

celery = Celery('trader')

celery.conf.update(
    # broker_url = 'redis://localhost:6379/0',
    broker_url = 'redis://redis:6379/0',
    # result_backend ='redis://localhost:6379/0',
    result_backend ='redis://redis:6379/0',
    imports = (
        'tasks'
    )
)