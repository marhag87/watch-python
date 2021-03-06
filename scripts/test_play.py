#!/usr/bin/env python3

import unittest
import sys
import os
import stat
import time
import mock

import play
from play import generate_play_command, create_control_file, remove_control_file, get, set, command, socketfile, help
from play import main as play_main
from mpv import mpv_control

class TestPlayInterface(unittest.TestCase):

  @mock.patch('play.play')
  def test_should_assume_only_one_arg_means_play(self, mock_main):
    url = 'https://www.youtube.com/watch?v=5u3iv8AT8G8'
    play_main(['play.py', url])

    mock_main.assert_called_with(url)

  def test_playing_file_returns_sane_command(self):
    play_command = generate_play_command(sys.argv[0])
    sane_command = [
      'mpv',
      '-x11-name', 'tv',
      '--mute=no',
      '--alang=jpn',
      '--idle=no',
      '',
      '--input-unix-socket', socketfile,
      sys.argv[0]
    ]

    self.assertEqual(sane_command, play_command)

  def test_should_be_able_to_start_mpv_in_idle_mode(self):
    play_command = generate_play_command(sys.argv[0], idle=True)

    self.assertIn('--idle=yes', play_command)

  def test_should_be_able_to_start_mpv_in_mute_mode(self):
    play_command = generate_play_command(sys.argv[0], mute=True)

    self.assertIn('--mute=yes', play_command)

  def test_should_be_able_to_start_mpv_in_novideo_mode(self):
    play_command = generate_play_command(sys.argv[0], video=False)

    self.assertIn('--no-video', play_command)

  def test_should_create_and_remove_control_file(self):
    # Remove existing file
    remove_control_file()
    with self.assertRaises(FileNotFoundError):
      stat.S_ISFIFO(os.stat(socketfile).st_mode)

    # Create new file
    create_control_file()
    self.assertEqual(stat.S_ISFIFO(os.stat(socketfile).st_mode), True)

    # Remove it again
    remove_control_file()
    with self.assertRaises(FileNotFoundError):
      stat.S_ISFIFO(os.stat(socketfile).st_mode)

  def test_command_should_fail_if_fifo_file_is_absent(self):
    remove_control_file()
    mpv = mpv_control()

    with self.assertRaises(FileNotFoundError):
      mpv.setup_socket(socketfile)

    mpv.teardown_socket()

  def test_can_send_commands_through_fifo(self):
    play.play('https://www.youtube.com/watch?v=B1WiYtAfNoQ', mute=True, video=False, pause_spotify=False)
    time.sleep(2)

    pause = get('pause')
    self.assertEqual(pause, False)

    set('pause', 'yes')
    pause = get('pause')
    self.assertEqual(pause, True)

    command('quit')
    with self.assertRaises(ConnectionRefusedError):
      get('pause')

  def test_should_be_able_to_play_http_content(self):
    play_command = generate_play_command('https://www.youtube.com/watch?v=5u3iv8AT8G8')

    self.assertIn('https://www.youtube.com/watch?v=5u3iv8AT8G8', play_command)

  @mock.patch('play.os')
  def test_directory_should_play_rar(self, mock_os):
    mock_os.path.isdir.return_value = True
    mock_os.listdir.return_value = ['myfile.r00', 'myfile.rar']
    result = play.get_actual_file('mydir')

    self.assertEqual(result, 'mydir/myfile.rar')

  @mock.patch('play.os')
  def test_file_should_play_directly(self, mock_os):
    mock_os.path.isdir.return_value = False
    result = play.get_actual_file('myfile.mkv')

    self.assertEqual(result, 'myfile.mkv')

if __name__ == '__main__':
  unittest.main()
