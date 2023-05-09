import time

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    LIST_STATUSES = (
        ('QUEUED', 'Queued'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # We could add more fields to this model to track more types of tasks
    # But for the simplicity, we will only track the number of items as we only have one type of task for this example

    number_of_items = models.PositiveIntegerField()
    count_done_items = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=255, default='QUEUED', choices=LIST_STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def done_percentage(self):
        return (self.count_done_items / self.number_of_items) * 100


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def long_run_process(cls, name, description):
        """A method that simulates a long-running process
        """
        time.sleep(2)
        instance = cls.objects.create(name=name, description=description)
        return instance
