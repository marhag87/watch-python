#!/usr/bin/env python3

import unittest
import mock
import os

from sort import move, get_next_episode, link_next_episode

class TestSort(unittest.TestCase):

  @mock.patch('sort.shutil')
  def test_files_from_other_folders_are_NOT_moved(self, mock_shutil):
    filename = '/tmp/test_file'
    move(filename)

    self.assertFalse(mock_shutil.move.called)

  @mock.patch('sort.shutil')
  def test_web_files_are_NOT_moved(self, mock_shutil):
    filename = 'https://www.youtube.com/watch?v=B1WiYtAfNoQ'
    move(filename)

    self.assertFalse(mock_shutil.move.called)

  @mock.patch('sort.os')
  def test_can_find_next_episode(self, mock_os):
    mock_os.walk.return_value = [
      (
        (),
        (),
        ('Physician.Which.2005.S08E03.720p.HDTV.x264-FoV.mkv',
         'Physician.Which.2005.S08E02.720p.HDTV.x264-FoV.mkv',
         'Physician.Which.2005.S08E01.720p.HDTV.x264-FoV.mkv',
         'Physician.Which.2005.S08E04.720p.HDTV.x264-FoV.mkv'
        ),
      ),
    ]

    next_episode = get_next_episode('Physician.Which.2005.S08E02.720p.HDTV.x264-FoV.mkv', 'Physician Which')

    self.assertEqual(next_episode, 'Physician.Which.2005.S08E03.720p.HDTV.x264-FoV.mkv')

  @mock.patch('sort.os')
  def test_doesnt_shit_itself_if_no_episodes(self, mock_os):
    mock_os.walk.return_value = [((),(),(),),]

    next_episode = get_next_episode('Physician.Which.2005.S08E02.720p.HDTV.x264-FoV.mkv', 'Physician Which')

    self.assertEqual(next_episode, None)

  @mock.patch('sort.os.path')
  @mock.patch('sort.os')
  def test_only_unlink_symlinks(self, mock_ospath, mock_os):
    mock_ospath.path.islink.return_value = True

    mock_os.walk.return_value = [
      (
        (),
        (),
        ('My Teacher Has a Horse-face 01.mkv',
         'next',
        ),
      ),
    ]

    link_next_episode('My Teacher Has a Horse-face 01.mkv')

    self.assertFalse(mock_os.unlink.called)

if __name__ == '__main__':
  unittest.main()
