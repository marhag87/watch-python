#!/usr/bin/env python3

import mock
import time
import urllib

from .base import FunctionalTest
from selenium import webdriver
from watch.shows import path

class NewVisitorTest(FunctionalTest):

  @mock.patch('watch.shows.os.path')
  @mock.patch('watch.shows.os')
  def test_can_start_watching_an_episode(self, mock_os, mock_ospath):
    mock_os.walk.side_effect = [
      [
        (
          (),
          ('Attraction Collapse', 'Top Kek', 'Bugwrangler', 'My Teacher Has a Horse-head'),
          (),
        ),
      ],
      [
        (
          (),
          (),
          ('Top.Kek.S01E01.mkv','Top.Kek.S01E02.mkv','Top.Kek.S01E03.mkv'),
        ),
      ],
    ]
    mock_ospath.realpath.return_value = path + '/Top Kek/Top.Kek.S01E02.mkv'
    # Joe wants to watch an episode of his favorite
    # show. He goes to the site.
    self.browser.get(self.server_url)

    # He notices the page title
    self.assertIn("Martin's Kickass Watch List", self.browser.title)

    # He also sees that there are many shows
    shows = self.browser.find_elements_by_class_name('show')
    allshows = ['Attraction Collapse', 'Top Kek', 'Bugwrangler', 'My Teacher Has a Horse-head']
    for myshow in allshows:
      self.assertIn(myshow, [show.get_attribute('data-show') for show in shows])

    # Not seeing the show he wants to watch instantly, he
    # tries searching for it
    # Now, the only show showing is the one Joe wans to see.
    filterbox = self.browser.find_element_by_id('filterbox')
    time.sleep(1)
    filterbox.send_keys('Top Kek')
    shows = self.browser.find_elements_by_class_name('show')
    for show in shows:
      if show.get_attribute('data-show') == 'Top Kek':
        self.assertEqual(show.is_displayed(), True)
      else:
        self.assertEqual(show.is_displayed(), False)

    # He clicks it and finds himself on a new page for the show
    # with all the available episodes listed
    self.browser.find_element_by_css_selector('[data-show="Top Kek"] .showlink').click()
    topkek_url = self.browser.current_url
    self.assertRegex(topkek_url, '/show/Top%20Kek')

    # He decides to watch the first episode he hasn't seen, which is marked green
    next_episode = self.browser.find_element_by_class_name('next_episode')
    self.assertEqual(next_episode.value_of_css_property('background-color'), 'rgba(0, 128, 0, 1)')

    # Having watched the show, Joe is satisfied and goes to sleep
