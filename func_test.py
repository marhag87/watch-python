#!/usr/bin/env python3

import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from time import sleep

from play import main, get, help

class TestMpvScript(unittest.TestCase):

  def test_script_can_play_video(self):
    # Joe wants to play a video, he runs the script
    # with no commands and gets instructions on how to run in
    out = StringIO()
    with redirect_stdout(out):
      main()

    self.assertEqual(help, out.getvalue().strip())

    # After seeing the help, he tries to play a video, but
    # he enters a filename that doesn't exist and gets an error
    filename = 'sjgjhsgfjhvajhasjhfv'
    with self.assertRaises(FileNotFoundError):
      main(['play.py', filename])

    # Joe plays a file that exists
    filename = 'https://www.youtube.com/watch?v=B1WiYtAfNoQ'
    main(['play.py', filename])
    sleep(2)

    path = get('path')
    self.assertEqual(filename, path)

    # Joe needs to get a drink, so he pauses the video
    main(['play.py', 'pause'])
    sleep(1)

    paused = get('pause')
    self.assertEqual(True, paused)

    # Having lost interest in the video, Joe wants to know how long is left
    out = StringIO()
    with redirect_stdout(out):
      main(['play.py', 'get', 'percent-pos'])
    sleep(1)

    self.assertIsInstance(out.getvalue().strip(), str)

    # Not wanting to watch any longer, Joe stops the video
    main(['play.py', 'stop'])

  def test_files_get_sorted(self):
    # After Joe has played a file from /home/$USER/series/, it
    # shows up in /home/$USER/series/Seen/
    path = '/home/' + os.getlogin() + '/series/'
    file = 'test_file'
    filename = path + file
    new_filename = path + 'Seen/' + file
    open(filename, 'a').close()

    main(['play.py', filename])
    sleep(1)

    self.assertTrue(os.path.isfile(new_filename))

    sleep(1) # Give it some time to clean up
    os.remove(new_filename)

if __name__ == '__main__':
  unittest.main()
