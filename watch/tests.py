#!/usr/bin/env python3

from django.test import TestCase
import mock

from watch.shows import get_shows, get_episodes, get_next_episode, path
from watch.views import command as view_command

class HomePageTest(TestCase):

  def test_home_page_renders_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_should_have_a_title(self):
    response = self.client.get('/')
    self.assertContains(response, "Martin's Kickass Watch List")

class ShowTest(TestCase):

  def test_show_page_renders_show_template(self):
    response = self.client.get('/show/Top Kek')
    self.assertTemplateUsed(response, 'show.html')

  def test_show_page_gives_404_if_no_show_specified(self):
    response = self.client.get('/show/')
    self.assertEqual(response.status_code, 404)

  def test_shows_should_come_back_sorted(self):
    shows = get_shows()
    shows_sorted = list(shows)
    shows_sorted.sort()

    self.assertEqual(shows, shows_sorted)

  @mock.patch('watch.shows.os')
  def test_should_return_shows(self, mock_os):
    mock_os.walk.return_value = [
      (
        (),
        ('Attraction Collapse', 'Top Kek', 'Finished', 'Seen'),
        (),
      ),
    ]
    response = self.client.get('/')
    self.assertContains(response, 'Attraction Collapse')
    self.assertContains(response, 'Top Kek')
    self.assertNotContains(response, 'Finished')
    self.assertNotContains(response, 'Seen')

  @mock.patch('watch.shows.os')
  def test_should_return_shows_even_if_seen_and_finished_are_not_present(self, mock_os):
    mock_os.walk.return_value = [
      (
        (),
        ('Attraction Collapse', 'Top Kek'),
        (),
      ),
    ]
    response = self.client.get('/')
    self.assertContains(response, 'Attraction Collapse')
    self.assertContains(response, 'Top Kek')

class EpisodeTest(TestCase):

  @mock.patch('watch.shows.os')
  def test_shows_should_get_episodes(self, mock_os):
    episodes = ('Attraction.Collapse.S01E01.mkv','Attraction.Collapse.S01E02.mkv')
    mock_os.walk.return_value = [
      (
        (),
        (),
        episodes,
      ),
    ]
    result_episodes = get_episodes('Attraction Collapse')
    self.assertEqual(list(episodes), result_episodes)

  @mock.patch('watch.shows.os')
  def test_episodes_should_come_back_sorted(self, mock_os):
    episodes = ('Attraction.Collapse.S01E02.mkv','attraction.collapse.s01e01.mkv')
    mock_os.walk.return_value = [
      (
        (),
        (),
        episodes,
      ),
    ]
    result_episodes = get_episodes('Attraction Collapse')
    episodes = list(episodes)
    self.assertEqual(['attraction.collapse.s01e01.mkv', 'Attraction.Collapse.S01E02.mkv'], result_episodes)

  @mock.patch('watch.shows.os')
  def test_episodes_should_not_return_the_next_file(self, mock_os):
    episodes = ('attraction.collapse.s01e01.mkv','Attraction.Collapse.S01E02.mkv')
    mock_os.walk.return_value = [
      (
        (),
        (),
        episodes + ('next',),
      ),
    ]
    result_episodes = get_episodes('Attraction Collapse')
    self.assertEqual(list(episodes), result_episodes)

class NextEpisodeTest(TestCase):

  @mock.patch('watch.shows.os.path')
  def test_next_episode_should_return_an_episode(self, mock_ospath):
    episodes = ('Attraction.Collapse.S01E01.mkv','Attraction.Collapse.S01E02.mkv')
    mock_ospath.realpath.return_value = path + 'Attraction Collapse/Attraction.Collapse.S01E01.mkv'

    next_episode = get_next_episode('Attraction Collapse')
    self.assertTrue(next_episode in episodes)

  @mock.patch('watch.shows.os.path')
  def test_next_episode_should_only_return_a_real_file(self, mock_ospath):
    mock_ospath.realpath.return_value = path + 'Attraction Collapse/jkdshkjhskdjgh'
    mock_ospath.isfile.return_value = False
    next_episode = get_next_episode('Attraction Collapse')

    self.assertEqual(next_episode, None)

class MediaButtonsTest(TestCase):

  @mock.patch('watch.views.mkvcommand')
  def test_valid_command_should_have_empty_response(self, mock_mkvcommand):
   response = view_command('', 'pause')
   self.assertEqual(response.status_code, 200)
   self.assertEqual(response.content, b'')

  def test_invalid_command_should_give_error(self):
   response = view_command('', 'blargh')
   self.assertEqual(response.status_code, 400)
   self.assertEqual(response.content, b'Invalid command') 
