"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll
from polls.forms import PollVoteForm


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


class HomePageViewTest(TestCase):

    def test_root_url_shows_all_polls(self):
        # setup some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/')

        # Converts bytes to string
        content = response.content.decode('UTF-8')
        self.assertIn(poll1.question, content)
        self.assertIn(poll2.question, content)

    def test_root_url_shows_links_to_all_polls(self):
        # setup some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/')

        # Check we have use the right template
        self.assertTemplateUsed(response, 'home.html')

        # Check we have passed the polls to the template
        polls_in_context = response.context['polls']
        self.assertEqual(list(polls_in_context), [poll1, poll2])

        # Converts bytes to string
        content = response.content.decode('UTF-8')
        self.assertIn(poll1.question, content)
        self.assertIn(poll2.question, content)

        # Check the page also contains the urls to individual polls pages
        poll1_url = reverse('polls.views.poll', args=[poll1.id, ])
        self.assertIn(poll1_url, content)
        poll2_url = reverse('polls.views.poll', args=[poll2.id, ])
        self.assertIn(poll2_url, content)


class SinglePollViewTest(TestCase):

    def test_page_shows_poll_title_and_no_votes_message(self):
        # Setup two polls, to check the right one is displayed
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/poll/%d/' % (poll2.id, ))

        # Check we have used the poll tempate
        self.assertTemplateUsed(response, 'poll.html')

        # Check we have passed the right poll into the context
        self.assertEqual(response.context['poll'], poll2)

        # Check the poll's question appears on the page
        content = response.content.decode('UTF-8')
        self.assertIn(poll2.question, content)

        # Check our 'no votes yet' message appears
        self.assertIn('No-one has voted on this poll yet', content)


class PollsVoteFormTest(TestCase):

    def test_form_renders_poll_choices_as_radio_inputs(self):
        # Setup a poll with a couple of choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
        choice2.save()

        # Setup another poll to make sure we only see the right choices
        poll2 = Poll(question='time', pub_date=timezone.now())
        poll2.save()
        choice3 = Choice(poll=poll2, choice='PM', votes=0)
        choice3.save()

        # build a voting form for poll1
        form = PollVoteForm(poll=poll1)

        self.assertEqual(list(form.fields.keys()), ['vote'])

        self.assertEqual(form.fields['vote'].choices, [
            (choice1.id, choice1.choice),
            (choice2.id, choice2.choice),
        ])

        # Check it uses radio inputs to render
        self.assertIn('type="radio"', form.as_p())

    def test_page_shows_choices_using_form(self):
        # Setup a poll with choices
        poll1 = Poll(question='time', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='PM', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice="Gardener's", votes=0)
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll1.id, ))

        # Check we have passed a form of the right type
        self.assertTrue(isinstance(response.context['form'], PollVoteForm))

        content = response.content.decode('UTF-8').replace('&#39;', "'")
        self.assertIn(choice1.choice, content)
        self.assertIn(choice2.choice, content)
