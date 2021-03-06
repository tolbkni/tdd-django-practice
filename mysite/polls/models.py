from django.db import models


# Create your models here.
class Poll(models.Model):

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return self.question

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())


class Choice(models.Model):

    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        try:
            return round(100 * self.votes / total_votes_on_poll, 2)
        except ZeroDivisionError:
            return round(0, 2)

