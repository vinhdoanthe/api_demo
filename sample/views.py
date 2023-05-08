from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes

from .models import Item, Task
from .serializers import TaskSerializer
from .tasks import create_an_item


@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def long_running_task(request, format=None):
    """
    A view that simulates a long-running task
    A task that create number_of_items of Item
    """
    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    for i in range(serializer.validated_data['number_of_items']):
        Item.long_run_process(name=f'Item {i}', description=f'Description {i}')

    return Response({'result': 'success'})


@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def tuned_long_running_task(request, format=None):
    """
    Long-running task with some tuning
    """
    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    task = serializer.save()

    for i in range(serializer.validated_data['number_of_items']):
        create_an_item.delay(name=f'Item {i}', description=f'Description {i}', task_id=task.id)

    return Response({
        'result': 'success',
        'data': {
            'task_id': task.id,
            'task_status': task.status,
        }
    })


@api_view(['GET'])
def get_long_running_task_status(request, task_id, format=None):
    """
    A view that get status of a long-running task
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'result': 'not found'}, status=404)

    return Response({
        'result': task.status,
        'done_percentage': task.done_percentage(),
        'list_done_items': task.list_done_items,
    })
