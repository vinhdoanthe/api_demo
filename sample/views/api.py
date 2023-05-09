from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from sample.decorators import one_active_request_only
from sample.models import Item, Task
from sample.serializers import WorkRequestDataSerializer
from sample.tasks import process_long_running_task


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def long_running_task(request, format=None):
    """
    A view that simulates a long-running task
    A task that create number_of_items of Item
    """
    serializer = WorkRequestDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'success': False,
                'message': serializer.errors
            }
        )

    for i in range(serializer.validated_data['number_of_items']):
        Item.long_run_process(name=f'Item {i}', description=f'Description {i}')

    return Response(
        status=status.HTTP_200_OK,
        data={
            'success': True,
            'message': 'Long-running task is done'
        }
    )


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@one_active_request_only
def long_running_task_with_tuning(request, format=None):
    """
    Long-running task with some tuning
    """
    serializer = WorkRequestDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'success': False,
                'message': serializer.errors
            }
        )

    # Create a task to track the progress of the long-running request
    task = Task.objects.create(
        user=request.user,
        number_of_items=serializer.validated_data['number_of_items']
    )

    process_long_running_task.delay(
        number_of_items=serializer.validated_data['number_of_items'],
        task_id=task.id
    )

    return Response(
        status=status.HTTP_200_OK,
        data={
            'success': True,
            'data': {
                'task_id': task.id,
                'task_status': task.status,
            }
    })


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_long_running_task_status(request, task_id, format=None):
    """
    A view that get status of a long-running task
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                'success': False,
                'message': 'Task not found'
            },
        )

    return Response(
        status=status.HTTP_200_OK,
        data={
            'success': True,
            'data': {
                'task_id': task.id,
                'task_status': task.status,
                'done_percentage': task.done_percentage(),
                'count_done_items': task.count_done_items,
            }
        }
    )

