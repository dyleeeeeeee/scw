from celery import shared_task
from .models import TaskModel
import time

@shared_task
def sample_task(data, timeout: int = 10):
    """"""
    created = TaskModel.objects.create(**data)
    print("Creating Task %s" % created)
    time.sleep(timeout)
    print("Done Task")
    return created