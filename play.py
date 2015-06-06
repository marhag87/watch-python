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

def control(arg):
  try:
    stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode)
    fifo = open('/tmp/mpv_control', 'w')
    fifo.write(arg + "\n")
    fifo.close()
  except:
    raise

def generate_play_command(name):
  if os.path.isfile(name):
    return ['mpv', '-x11-name', 'tv', '--mute=no', '--alang=jpn', '--input-file', '/tmp/mpv_control', name]
  else:
    raise FileNotFoundError('Could not find file: ' + name)


if __name__ == '__main__':
  if len(sys.argv) > 2:
    if sys.argv[1] == 'play':
      remove_control_file()
      create_control_file()
      subprocess.check_call(generate_play_command(sys.argv[2]))
      remove_control_file()
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'pause':
      control('cycle pause')
    if sys.argv[1] == 'stop':
      control('stop')
    if sys.argv[1] == 'next_chapter':
      control('add chapter 1')
    if sys.argv[1] == 'prev_chapter':
      control('add chapter -1')
