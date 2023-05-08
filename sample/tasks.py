from celery import shared_task

from django.db import transaction

from .models import Item, Task


@shared_task()
def create_an_item(name, description, task_id):
    """ A task that simulates a long-running process
    """
    instance = Item.long_run_process(name, description)  # This is our long-running process
    with transaction.atomic():
        try:
            task = Task.objects.select_for_update().get(task_id)
        except Task.DoesNotExist:
            return instance

        task.list_done_items += f'{instance.id},'
        if task.list_done_items.count(',') == task.number_of_items:
            task.status = 'SUCCESS'
        else:
            task.status = 'PROCESSING'
        task.save()
    return instance
