#!/usr/bin/env python3

import unittest
import mock
import os

from sort import move, sort_seen

class TestSort(unittest.TestCase):

  @mock.patch('sort.shutil')
  def test_files_from_series_folder_are_moved(self, mock_shutil):
    path = '/home/' + os.getlogin() + '/series/'
    file1 = 'test_file01'
    filename1 = path + file1
    file2 = 'test_file02'
    filename2 = path + file2

    move(filename1)
    mock_shutil.move.assert_called_with(filename1, path + 'Seen/' + file1)

    move(filename2)
    mock_shutil.move.assert_called_with(filename2, path + 'Seen/' + file2)

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
  def test_files_from_seen_folder_are_moved_to_respecive_series(self, mock_shutil):
    path = '/home/' + os.getlogin() + '/series/'
    file1 = 'test_file01'
    filename1 = path + 'Seen/' + file1
    file2 = 'test_file02'
    filename2 = path + 'Seen/' + file2

    sort_seen(filename1)
    mock_shutil.move.assert_called_with(filename1, path + 'test_file/test_file01')
    sort_seen(filename2)
    mock_shutil.move.assert_called_with(filename2, path + 'test_file/test_file02')

  @mock.patch('sort.shutil')
  def test_files_from_other_folders_are_NOT_sorted(self, mock_shutil):
    filename = '/home/' + os.getlogin() + '/series/test_file01'
    sort_seen(filename)

    self.assertFalse(mock_shutil.move.called)

  @mock.patch('sort.shutil')
  def test_web_files_are_NOT_sorted(self, mock_shutil):
    filename = 'https://www.youtube.com/watch?v=B1WiYtAfNoQ'
    sort_seen(filename)

    self.assertFalse(mock_shutil.move.called)

if __name__ == '__main__':
  unittest.main()
