#!/usr/bin/env python

import unittest
import sys
import os
import stat
from play import generate_play_command, create_control_file, remove_control_file

class TestPlayInterface(unittest.TestCase):

  def test_playing_file_returns_sane_command(self):
    play_command = generate_play_command(sys.argv[0])
    sane_command = [
      'mpv',
      '-x11-name', 'tv',
      '--mute=no',
      '--alang=jpn',
      '--input-file', '/tmp/mpv_control',
      sys.argv[0]
    ]

    self.assertEqual(sane_command, play_command)

  def test_should_check_that_file_exists(self):
    play_command1 = generate_play_command(sys.argv[0])

    self.assertIn(sys.argv[0], play_command1)

    with self.assertRaises(FileNotFoundError):
      play_command2 = generate_play_command('aksjghskjdhgkjsgdf')


  def test_should_create_and_remove_control_file(self):
    # Remove existing file
    remove_control_file()
    with self.assertRaises(FileNotFoundError):
      stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode)

    # Create new file
    create_control_file()
    self.assertEqual(stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode), True)

    # Remove it again
    remove_control_file()
    with self.assertRaises(FileNotFoundError):
      stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode)


if __name__ == '__main__':
  unittest.main()
