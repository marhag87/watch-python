#!/usr/bin/env python3

import unittest
import os
import mock
from io import StringIO
from contextlib import redirect_stdout
from time import sleep

from play import main, get, help
from sort import move, link_next_episode, path

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

  @mock.patch('sort.os.path')
  @mock.patch('sort.shutil')
  def test_files_are_moved_to_respecive_series(self, mock_shutil, mock_ospath):
    # After watching an episode, Joe notices that the file has been
    # moved to the appropriate folder for the series
    file1 = 'Attraction.Collapse.S02E04.720p.HDTV.x264-BATV.mkv'
    filename1 = path + file1
    file2 = 'Physician.Which.2005.S09E00.Last.Christmas.720p.HDTV.x264-FoV.mkv'
    filename2 = path + file2
    file3 = 'top.kek.s22e03.720p.HDTV.x264-ORGANiC.mkv'
    filename3 = path + file3
    file4 = '[TerribleConnotations] Demise Procession - 10 [720p].mkv'
    filename4 = path + file4
    file5 = '[TerribleConnotations] Bugwrangler S2 - 22 [720p].mkv'
    filename5 = path + file5
    file6 = '[What]_Cherry_Projectiles_-_01_[1280x720_H.264_AAC][1FBF88D2].mkv'
    filename6 = path + file6
    file7 = '[TerribleConnotations] My Teacher Has a Horse-head - 02 [1080p].mkv'
    filename7 = path + file7
    file8 = '[Coalgirls]_Hunter_X_Hunter_117_(1920x1080_Blu-ray_FLAC)_[8056C087].mkv'
    filename8 = path + file8
    file9 = 'My Teacher Has a Horce-face 01.mkv'
    filename9 = path + file9
    mock_ospath.realpath.side_effect = [ path + file1, path + file2, path + file3, path + file4, path + file5, path + file6, path + file7, path + file8, path + file9, ]

    move(filename1)
    mock_shutil.move.assert_called_with(filename1, path + 'Attraction Collapse/' + file1)
    move(filename2)
    mock_shutil.move.assert_called_with(filename2, path + 'Physician Which/' + file2)
    move(filename3)
    mock_shutil.move.assert_called_with(filename3, path + 'Top Kek/' + file3)
    move(filename4)
    mock_shutil.move.assert_called_with(filename4, path + 'Demise Procession/' + file4)
    move(filename5)
    mock_shutil.move.assert_called_with(filename5, path + 'Bugwrangler/' + file5)
    move(filename6)
    mock_shutil.move.assert_called_with(filename6, path + 'Cherry Projectiles/' + file6)
    move(filename7)
    mock_shutil.move.assert_called_with(filename7, path + 'My Teacher Has a Horse-head/' + file7)
    move(filename8)
    mock_shutil.move.assert_called_with(filename8, path + 'Hunter x Hunter/' + file8)
    move(filename9)
    mock_shutil.move.assert_called_with(filename9, path + 'My Teacher Has a Horce-face/' + file9)

  @mock.patch('sort.os')
  def test_link_to_next_episode_is_created(self, mock_os):
    # After watching an episode, Joe sees that the next episode has
    # been linked with the name "next" in the appropriate series folder
    file1 = 'Attraction.Collapse.S02E04.720p.HDTV.x264-BATV.mkv'
    next_episode = 'Attraction.Collapse.S02E05.720p.HDTV.x264-BATV.mkv'
    filename1 = path + file1
    mock_os.walk.return_value = [
      (
        (),
        (),
        (file1,
         next_episode,
        ),
      ),
    ]

    link_next_episode(file1)
    mock_os.unlink.assert_called_with(path + 'Attraction Collapse/next')
    mock_os.symlink.assert_called_with(path + 'Attraction Collapse/' + next_episode, path + 'Attraction Collapse/next')

  @mock.patch('sort.os')
  def test_link_to_next_episode_is_not_created_if_its_the_last_episode(self, mock_os):
    # Having finished all episodes, Joe notices that there no longer is a
    # "next" link
    file1 = 'Attraction.Collapse.S02E04.720p.HDTV.x264-BATV.mkv'
    filename1 = path + 'Attraction Collapse/' + file1
    mock_os.walk.return_value = [
      (
        (),
        (),
        (file1,
         'next',
        ),
      ),
    ]

    link_next_episode(file1)
    mock_os.unlink.assert_called_with(path + 'Attraction Collapse/next')
    self.assertFalse(mock_os.symlink.called)

if __name__ == '__main__':
  unittest.main()
