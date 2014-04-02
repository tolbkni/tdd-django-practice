# Create your views here.

from django.shortcuts import render
from polls.models import Poll


def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)


def poll(request, poll_id):
    context = {'poll': Poll.objects.get(pk=poll_id)}
    return render(request, 'poll.html', context)
