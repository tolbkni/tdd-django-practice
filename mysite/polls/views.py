# Create your views here.

from django.shortcuts import render
from polls.models import Poll
from polls.forms import PollVoteForm


def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)


def poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    form = PollVoteForm(poll=poll)
    context = {'poll': poll, 'form': form}
    return render(request, 'poll.html', context)
