#!/usr/bin/env python3

import sys
import os
import stat
import subprocess
from control_spotify import control_spotify
from mpv import mpv_control

def create_control_file():
  os.mkfifo('/tmp/mpv_control')

def remove_control_file():
  try:
    stat.S_ISFIFO(os.stat('/tmp/mpv_control').st_mode)
    os.remove('/tmp/mpv_control')
  except:
    pass

def generate_play_command(name, idle=False, mute=False):
  if os.path.isfile(name) or name.startswith('http'):
    idle = 'yes' if idle else 'no'
    mute = 'yes' if mute else 'no'
    return ['mpv', '-x11-name', 'tv', '--mute=' + mute, '--alang=jpn', '--idle=' + idle, '--input-unix-socket', '/tmp/mpv_control', name]
  else:
    raise FileNotFoundError('Could not find file: ' + name)

def play(file, idle=False, mute=False):
  control_spotify('Pause')
  remove_control_file()
  create_control_file()
  subprocess.Popen(generate_play_command(file, idle=idle, mute=mute), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get(prop):
  mpv = mpv_control()
  mpv.setup_socket('/tmp/mpv_control')
  result = mpv.get(prop)
  mpv.teardown_socket()
  return result

def set(prop, value):
  mpv = mpv_control()
  mpv.setup_socket('/tmp/mpv_control')
  result = mpv.set(prop, value)
  mpv.teardown_socket()
  return result

def command(com):
  mpv = mpv_control()
  mpv.setup_socket('/tmp/mpv_control')
  mpv.command(com)
  mpv.teardown_socket()

if __name__ == '__main__':
  if len(sys.argv) > 2:
    if sys.argv[1] == 'play':
      play(sys.argv[2])
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'pause':
      command('cycle pause')
    elif sys.argv[1] == 'stop':
      command('stop')
    elif sys.argv[1] == 'next_chapter':
      command('add chapter 1')
    elif sys.argv[1] == 'prev_chapter':
      command('add chapter -1')
