from django.shortcuts import render

from sample.forms import WorkRequestForm


def index(request):
    return render(request, 'index.html')


def submit_default(request):
    task_form = WorkRequestForm(initial={'number_of_items': 3})
    return render(request, 'submit_default.html', context={
        'task_form': task_form,
    })


def submit_with_tuning(request):
    task_form = WorkRequestForm(initial={'number_of_items': 3})
    return render(request, 'submit_with_tuning.html', context={
        'task_form': task_form,
    })
