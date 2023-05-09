from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from sample.forms import WorkRequestForm


def index(request):
    return render(request, 'index.html')


@login_required
def submit_default(request):
    if request.method == "GET":
        task_form = WorkRequestForm(initial={'number_of_items': 3})
        return render(request, 'submit_default.html', context={
            'task_form': task_form,
        })
    else:
        return HttpResponseBadRequest()


@login_required()
def submit_with_tuning(request):
    if request.method == "GET":
        task_form = WorkRequestForm(initial={'number_of_items': 3})
        return render(request, 'submit_with_tuning.html', context={
            'task_form': task_form,
        })
    else:
        return HttpResponseBadRequest()
