# Create your views here.

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from polls.models import Choice, Poll
from polls.forms import PollVoteForm


def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)


def poll(request, poll_id):
    if request.method == 'POST':
        choice = Choice.objects.get(id=request.POST['vote'])
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls.views.poll', args=[poll_id, ]))

    poll = Poll.objects.get(pk=poll_id)
    form = PollVoteForm(poll=poll)
    context = {'poll': poll, 'form': form}
    return render(request, 'poll.html', context)
