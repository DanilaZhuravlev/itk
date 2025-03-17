from django.db import transaction
from .models import TaskQueue

@transaction.atomic
def fetch_task():
    task = TaskQueue.objects.filter(status='pending').select_for_update().first()
    if task:
        task.status = 'in_progress'
        task.save()
        return task
    return None