from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll


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

    def test_view_shows_percentage_of_votes(self):
        # Setup a poll with choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=1)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answser', votes=2)
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll1.id, ))

        content = response.content.decode('UTF-8')
        # Check the percentages of votes are shown, sensibly rounded
        self.assertIn('33 %: 42', content)
        self.assertIn('67 %: The Ultimate Answer', content)

        # And the 'no-one has voted' message is gone
        self.assertNotIn('No-one has voted', content)

    def test_choice_can_calculate_its_own_percentage_of_votes(self):
        poll1 = Poll(question='who?', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='me', votes=2)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='you', votes=1)
        choice2.save()

        self.assertEqual(choice1.percentage(), 100 * 2 / 3.0)
        self.assertEqual(choice2.percentage(), 100 * 1 / 3.0)

        # Also check 0-vote case
        choice1.votes = 0
        choice1.save()
        choice2.votes = 0
        choice2.save()

        self.assertEqual(choice1.percentage(), 0)
        self.assertEqual(choice2.percentage(), 0)

    def test_view_can_handle_vote_via_post(self):
        # Setup a poll with choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=1)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answser', votes=3)
        choice2.save()

        # Setup our POST data
        post_data = {'vote': str(choice2.id)}

        # Make our request to the view
        poll_url = '/poll/%d/' % (poll1.id, )
        response = self.client.post(poll_url, data=post_data)

        # Retrieve the updated choice from the database
        choice_in_db = Choice.objects.get(pk=choice2.id)

        # Check it's votes have gone up by 1
        self.assertEqual(choice_in_db.votes, 4)

        # Always redirect after a POST - even if, in this case, we go back
        # to the same page.
        self.assertRedirects(response, poll_url)
