#!/usr/bin/env python3

import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from time import sleep

from play import main, get, help
from sort import sort_seen

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
    # shows up in the appropriate folder for that show
    path = '/home/' + os.getlogin() + '/series/'
    file = 'test_file01'
    filename = path + file
    new_filename = path + 'test_file/' + file
    open(filename, 'a').close()
    direxists = os.path.exists(path + 'test_file')
    if not direxists:
      os.makedirs(path + 'test_file')

    main(['play.py', filename])
    sleep(1)
    sort_seen(path + 'Seen/' + file) # This should be done in the main script, but I don't dare adding it there yet
    sleep(1)

    self.assertTrue(os.path.isfile(new_filename))

    sleep(1) # Give it some time to clean up
    os.remove(new_filename)
    if not direxists:
      os.rmdir(path + 'test_file')

if __name__ == '__main__':
  unittest.main()
