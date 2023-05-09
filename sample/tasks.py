from celery import shared_task

from .models import Item, Task


@shared_task()
def process_long_running_task(number_of_items, task_id):
    """ Process a long-running task
    """
    Task.objects.filter(id=task_id).update(status='PROCESSING')

    for i in range(number_of_items):
        Item.long_run_process(name=f'Item {i}', description=f'Description {i}')
        Task.objects.filter(id=task_id).update(count_done_items=i + 1)

    Task.objects.filter(id=task_id).update(status='SUCCESS')
    return True
