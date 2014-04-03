from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from polls.models import Poll


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
