# Build a sample API

## Requirements
![Requirements](./docs/requirement.png)

## How to use
<a href="https://www.loom.com/share/0054ec62aec8462dbb2f7ee22c12e1b4">
    <p>Demo: Django API with client long-polling request to update status - Watch Video</p>
    <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/0054ec62aec8462dbb2f7ee22c12e1b4-with-play.gif">
</a>

### Demo system
URL: https://savvy-demo-api-6nkxh.ondigitalocean.app/  
Username: demo  
Password: demo@123

## How to run
1. Clone this repository and go to the project folder
2. Create `.env` file with content like `.env.example`, `.env.docker` file with content like `.env.docker.example`, `.env.postgresql` file with content like `.env.postgresql.example`
```bash
cp .env.example .env
cp .env.docker.example .env.docker
cp .env.postgresql.example .env.postgresql
```
   
3. Build docker image and run docker container
```bash
docker-compose build
docker-compose up
```
4. Access to the `web` container and run `python manage.py migrate` to migrate database
5. Access to the `web` container and create a new user with command `python manage.py createsuperuser`
6. Open `http://localhost:8000` and login with the user you just created

## Project explanation
Assume that each item in loop need 2 seconds to process by creating the function `long_run_process` in the `Item` model.
```python
    @classmethod
    def long_run_process(cls, name, description):
        """A method that simulates a long-running process
        """
        time.sleep(2)
        instance = cls.objects.create(name=name, description=description)
        return instance
```
We solve the problem by:
* Use Celery to process the long-running task asynchronously
* Use the Task model to track the progress of the long-running task
* Create 2 APIs (using Django Rest Framework): one for main request and one for getting the status of the long-running task
### The `Task` model
Task model has fields for tracking the progress of the task and has `user` field to protect server against users submitting parallel requests. See the `Task` model in `sample/models.py` for more details.

### Main request
`POST api/tuned-long-running-task/` to receive the request data, create a task record for this request, send the long-running progress to Celery, then response the task id.
```python
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
```
We also write a decorator for this API to protect server against users submitting parallel requests (only one active request at a time).
```python
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
```
In the Celery, we update the status of the task when each item is processed. If all items are processed, we update the status of the task to `SUCCESS`.
```python
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
```
### Get the status of the task
`GET api/tuned-long-running-task/<task_id>/` to get the status of a task by task id.
```python
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
                'number_of_items': task.number_of_items,
            }
        }
    )
```

### Client side
It's separated into 2 parts:
* Send the main request and get the task id
* Get the status of the task by task id and update the progress bar periodically

Users will be able to see that the request is processing. It makes a better user experience.

### Other considerations
* Use `Django Channels` (WebSocket) for updating the progress bar in real-time
* We could use Redis to store the task status instead of using the database
* The logic to check the uniqueness of the request could be changed by using hash function of request data