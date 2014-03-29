"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from polls.models import Poll


class PollModelTest(TestCase):

    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()

        # check if we can save it to the database
        poll.save()

        # check we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEqual(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEqual(only_poll_in_database, poll)

        # check that it's saved question and pub_date
        self.assertEqual(only_poll_in_database.question, "What's up?")
        self.assertEqual(only_poll_in_database.pub_date, poll.pub_date)

    def test_verbose_name_for_pub_date(self):
        for field in Poll._meta.fields:
            if field.name == 'pub_date':
                self.assertEqual(field.verbose_name, 'Date published')
