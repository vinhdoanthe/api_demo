from datetime import datetime, timedelta

from .models import Task

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


def one_active_request_only(function):
    """A decorator that prevents a user from sending multiple requests at the same time
    """
    def wrap(request, *args, **kwargs):
        task = Task.objects.filter(
            user=request.user,
            status__in=['QUEUED', 'PROCESSING'],
            created_at__gt=timezone.now() - timedelta(minutes=5)
        )  # Check if there is an active request. The logic here depends on the business requirement

        if not task:
            return function(request, *args, **kwargs)
        else:
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'success': True,
                    'message': 'There is an active request',
                    'data': {
                        'task_id': task.first().id,
                    }
                }
            )

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
