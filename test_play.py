#!/usr/bin/env python

import unittest
import sys
import os
import stat
from play import generate_play_command, create_control_file, remove_control_file, control

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

  def test_command_should_fail_if_fifo_file_is_absent(self):
    remove_control_file()
    with self.assertRaises(FileNotFoundError):
      control('wat')

  def test_can_send_commands_through_fifo(self):
    remove_control_file()
    create_control_file()
    pid = os.fork()
    if pid:
      fifo = open('/tmp/mpv_control', 'r')
      result = fifo.read()
      fifo.close()
      self.assertEqual('wat\n', result)
    else:
      control('wat')
      # Use os instead of sys. This skips cleanups but doesn't raise errors
      os._exit(0)


if __name__ == '__main__':
  unittest.main()
