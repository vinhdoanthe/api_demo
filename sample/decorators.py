from .models import Task

from rest_framework import status
from rest_framework.response import Response


def one_active_request_only(function):
    def wrap(request, *args, **kwargs):
        task = Task.objects.filter(
            user=request.user,
            status__in=['QUEUED', 'PROCESSING']
        )
        if not task:
            return function(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'success': False,
                                'message': 'There is an active request'
                            })
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
