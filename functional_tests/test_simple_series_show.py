#!/usr/bin/env python3

import mock
import time
import urllib
import sys

sys.path.insert(0, 'scripts')

from .base import FunctionalTest
from selenium import webdriver
from watch.shows import path

class NewVisitorTest(FunctionalTest):

  @mock.patch('watch.views.mkvplay')
  @mock.patch('watch.shows.os.path')
  @mock.patch('watch.shows.os')
  def test_can_start_watching_an_episode(self, mock_os, mock_ospath, mock_play):
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
    mock_ospath.isfile.return_value = True
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
    self.assertEqual(next_episode.value_of_css_property('background-color'), 'rgba(230, 230, 230, 1)')
    next_episode.find_element_by_css_selector('a').click()
    episode_url = self.browser.current_url
    self.assertEqual(episode_url, 'http://localhost:8081/show/Top%20Kek')

    mock_play.assert_called_with(path + 'Top Kek/Top.Kek.S01E02.mkv')

    # Having watched the show, Joe is satisfied and goes to sleep

  @mock.patch('watch.views.mkvcommand')
  def test_can_use_media_buttons(self, mock_command):
    # Joe starts watching an episode
    self.browser.get(self.server_url)

    # Having seen the intro before he wants to skip it,
    # he presses the "next chapter" button
    next_chapter = self.browser.find_element_by_id('nextchapter-button')
    next_chapter.click()
    time.sleep(1)

    mock_command.assert_called_with('add chapter 1')

    # He accidentaly clicks twice, so he clicks "prev chapter" button
    # to get back
    prev_chapter = self.browser.find_element_by_id('prevchapter-button')
    prev_chapter.click()
    time.sleep(1)

    mock_command.assert_called_with('add chapter -1')

    # Needing a toilet break, he pauses
    pause = self.browser.find_element_by_id('pause-button')
    pause.click()
    time.sleep(1)

    mock_command.assert_called_with('cycle pause')

    # Not feeling like watching anymore, he pushes the stop button
    stop = self.browser.find_element_by_id('stop-button')
    stop.click()
    time.sleep(1)

    mock_command.assert_called_with('stop')

  #def test_shit(self):
  #  playing an episode that isn't the next one (confirm)

  #  play next episode button

  #  remove "next" file

  #  statusbar (time left)

  #  episodes outside of show folder

  #  regex compiles?
  #  get_show on all files under path?

  #  buttons
  #    stop and don't advance
  #    etc
  #    probably mock
