"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll


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

    def test_poll_objects_are_named_after_their_question(self):
        poll = Poll()
        poll.question = 'How is babby formed?'
        # Python 2's unicode() was renamed str() in Python3
        self.assertEqual(str(poll), 'How is babby formed?')


class ChoiceModelTest(TestCase):

    def test_creating_some_choices_for_a_poll(self):
        # start by creating a new Poll object
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()
        poll.save()

        # create a Choice object
        choice = Choice()
        # Link it to our Poll object
        choice.poll = poll
        choice.choice = "doin' fine..."
        # It has some votes
        choice.votes = 3
        choice.save()

        poll_choices = poll.choice_set.all()
        self.assertEqual(poll_choices.count(), 1)

        choice_from_db = poll_choices[0]
        self.assertEqual(choice_from_db, choice)
        self.assertEqual(choice_from_db.choice, "doin' fine...")
        self.assertEqual(choice_from_db.votes, 3)

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEqual(choice.votes, 0)
