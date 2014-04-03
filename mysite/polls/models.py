from django.db import models


# Create your models here.
class Poll(models.Model):

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return self.question


class Choice(models.Model):

    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        try:
            return 100 * self.votes / total_votes_on_poll
        except ZeroDivisionError:
            return 0
