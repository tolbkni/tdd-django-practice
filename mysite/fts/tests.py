"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
