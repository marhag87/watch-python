#!/usr/bin/env python3

import unittest
import mock
import os

from sort import move, get_next_episode, link_next_episode, path

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

  @mock.patch('sort.shutil')
  def test_files_in_subfolder_are_not_moved(self, mock_shutil):
    move(path + 'Physician Which/Physician.Which.2005.S08E03.720p.HDTV.x264-FoV.mkv')

    self.assertFalse(mock_shutil.move.called)

  @mock.patch('os.path')
  @mock.patch('sort.shutil')
  def test_episodes_are_moved_when_finished(self, mock_shutil, mock_ospath):
    file = 'Physician.Which.2005.S08E03.720p.HDTV.x264-FoV.mkv'
    filename = path + file
    mock_ospath.realpath.return_value = filename
    move(filename)

    mock_shutil.move.assert_called_with(filename, path + 'Physician Which/' + file)

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

  @mock.patch('sort.os.path')
  @mock.patch('sort.shutil')
  def test_move_to_Seen_folder_if_one_for_series_doesnt_exist(self, mock_shutil, mock_ospath):
    e = FileNotFoundError('No such file or directory')
    mock_shutil.move.side_effect = [e, None]
    filename = 'Physician.Which.2005.S08E03.720p.HDTV.x264-FoV.mkv'
    mock_ospath.realpath.return_value = path + filename

    move(filename)
    mock_shutil.move.assert_called_with(path + filename, path + 'Seen/' + filename)

  @mock.patch('sort.os')
  def test_doesnt_shit_itself_if_no_episodes(self, mock_os):
    mock_os.walk.return_value = [((),(),(),),]

    next_episode = get_next_episode('Physician.Which.2005.S08E02.720p.HDTV.x264-FoV.mkv', 'Physician Which')

    self.assertEqual(next_episode, None)

  @mock.patch('sort.os.path')
  @mock.patch('sort.os')
  @mock.patch('sort.shutil')
  def test_removes_next_symlink_if_played(self, mock_shutil, mock_os, mock_ospath):
    filename = 'next'
    mock_ospath.realpath.return_value = path + 'My Teacher Has a Horce-face/My Teacher Has a Horse-face 01.mkv'
    mock_shutil.move.return_value = None
    mock_os.walk.return_value = [
      (
        (),
        (),
        ('My Teacher Has a Horse-face 01.mkv',
         filename,
        ),
      ),
    ]

    move(path + 'My Teacher Has a Horce-face/next')
    mock_os.unlink.assert_called_with(path + 'My Teacher Has a Horse-face/next')
    self.assertFalse(mock_os.symlink.called)

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
