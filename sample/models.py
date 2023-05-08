import time

from django.db import models


class Task(models.Model):

    LIST_STATUS = (
        ('QUEUED', 'Queued'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
    )

    number_of_items = models.PositiveIntegerField()
    list_done_items = models.TextField(default='')
    status = models.CharField(max_length=255, default='QUEUED', choices=LIST_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def done_percentage(self):
        return self.list_done_items.count(',') / self.number_of_items * 100


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def long_run_process(cls, name, description):
        """A method that simulates a long-running process
        """
        time.sleep(10)
        instance = cls.objects.create(name=name, description=description)
        return instance
