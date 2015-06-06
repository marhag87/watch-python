#!/usr/bin/env python3

import unittest
import mock
import os

from sort import move

class TestSort(unittest.TestCase):

  @mock.patch('sort.shutil')
  def test_files_from_series_folder_are_moved(self, mock_shutil):
    path = '/home/' + os.getlogin() + '/series/'
    file1 = 'test_file'
    filename1 = path + file1
    file2 = 'test_file2'
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

if __name__ == '__main__':
  unittest.main()
