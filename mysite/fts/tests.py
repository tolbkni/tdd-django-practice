"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium import webdriver


class PollsTest(LiveServerTestCase):

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

        # TODO use the admin site to create a Poll
        self.fail('finish this test')
