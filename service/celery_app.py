from celery import Celery
import os
import dotenv
# import sys
# sys.path.append('.')

# Load environment variables
dotenv.load_dotenv()

# Read environment variable to get the broker url
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

celery = Celery('trader')

celery.conf.update(
    broker_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # broker_url = 'redis://redis:6379/0',
    result_backend = f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # result_backend ='redis://redis:6379/0',
    imports = (
        'tasks'
    )
)