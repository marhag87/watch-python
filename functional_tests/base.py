#!/usr/bin/env python3

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class FunctionalTest(StaticLiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.server_url = cls.live_server_url

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()
