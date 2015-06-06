#!/usr/bin/env python

import sys
import os
import stat
import subprocess

def create_control_file():
  os.mkfifo('/tmp/mpv_control')

def remove_control_file():
  try:
    stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode)
    os.remove('/tmp/mpv_control')
  except:
    pass

def generate_play_command(name):
  if os.path.isfile(name):
    return ['mpv', '-x11-name', 'tv', '--mute=no', '--alang=jpn', '--input-file', '/tmp/mpv_control', name]
  else:
    raise FileNotFoundError('Could not find file: ' + name)


if __name__ == '__main__':
  if len(sys.argv) > 1:
    subprocess.check_call(generate_play_command(sys.argv[1]))
