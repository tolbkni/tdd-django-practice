from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll
from polls.forms import PollVoteForm


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
