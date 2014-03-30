"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from collections import namedtuple
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question='How awesome is Test-Driven Development?',
    choices=[
        'Very awesome',
        'Quite awesome',
        'Moderately awesome',
    ],
)
POLL2 = PollInfo(
    question="Which workshop treat do you prefer?",
    choices=[
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge',
    ],
)


class PollsTest(LiveServerTestCase):

    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Open browser, and go to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # Find 'Django administration' in body.text
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # Find a couple of hyperlink that says 'Polls'
        poll_links = self.browser.find_elements_by_link_text('Polls')
        # assertEquals is deprecated, use assertEqual instead of
        self.assertEqual(len(poll_links), 2)

        # Clicks the second hyperlink that says 'Polls'
        poll_links[1].click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 polls', body.text)

        # Find a hyperlink that says 'Add poll', and click it to add a poll
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()

        # Find some input fields for 'Question' and 'Date published'
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Date published:', body.text)

        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys('How awesome is Test-Driven Development?')

        # Sets date and time of the publication
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('01/01/12')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')

        # Adds three choices for the poll
        choice_0 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_0.send_keys('Very awesome')
        choice_1 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_1.send_keys('Quite awesome')
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Moderately awesome')

        # Clicks the button to save the poll
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        new_poll_links = self.browser.find_elements_by_link_text('How awesome is Test-Driven Development?')
        self.assertEqual(len(new_poll_links), 1)

        # Satisfied

    def _setup_polls_via_admin(self):
        # Logs into the admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # Enters a number of polls
        for poll_info in [POLL1, POLL2]:
            # Follows the link to the polls app, and adds a new poll
            polls_links = self.browser.find_elements_by_link_text('Polls')
            polls_links[1].click()
            add_poll_link = self.browser.find_element_by_link_text('Add poll')
            add_poll_link.click()

            # Enters question, uses today and now to set publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            self.browser.find_element_by_link_text('Today').click()
            self.browser.find_element_by_link_text('Now').click()

            for i, choice_text in enumerate(poll_info.choices):
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                choice_field.send_keys(choice_text)

            # Clicks the save button to save new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the 'Polls' listing, sees the new poll,
            # listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(poll_info.question)
            self.assertEqual(len(new_poll_links), 1)

            # Goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')

        # Logs out of the admin page
        log_out_link = self.browser.find_element_by_link_text('Log out')
        log_out_link.click()

    def test_voting_on_a_new_poll(self):
        # First, the administrator logs into the admin site and
        # creates a couple of new polls, and their response choices
        self._setup_polls_via_admin()

        # Now the regular user goes to the homepage of the site,
        # sees a list of polls
        self.browser.get(self.live_server_url)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(heading.text, 'Polls')

        # The regular user clicks on the link of the first poll,
        # which is called 'How awesome is test-driven development?'
        first_poll_title = POLL1.question
        first_poll_link = self.browser.find_element_by_link_text(first_poll_title)
        first_poll_link.click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEqual(sub_heading.text, first_poll_title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

        self.fail('TODO')
        # He also sees a form, which offers him several choices.
        # He decide to select 'very awesome'

        # He clicks 'submit'

        # The page refreshes, and he sees that his choice has updated
        # the results, they now say '100 %: very awesome'.

        # The page also says '1 votes'

        # Satisfied
