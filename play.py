#!/usr/bin/env python3

import sys
import os
import stat
import subprocess
from control_spotify import control_spotify
from mpv import mpv_control

socketfile = '/tmp/mpv_control'

def create_control_file():
  os.mkfifo(socketfile)

def remove_control_file():
  try:
    stat.S_ISFIFO(os.stat(socketfile).st_mode)
    os.remove(socketfile)
  except:
    pass

def generate_play_command(name, idle=False, mute=False, video=True):
  if os.path.isfile(name) or name.startswith('http'):
    idle = 'yes' if idle else 'no'
    mute = 'yes' if mute else 'no'
    video = '' if video else '--no-video'
    return ['mpv',
            '-x11-name', 'tv',
            '--mute=' + mute,
            '--alang=jpn',
            '--idle=' + idle,
            video,
            '--input-unix-socket', socketfile,
            name]
  else:
    raise FileNotFoundError('Could not find file: ' + name)

def play(file, idle=False, mute=False, video=True, pause_spotify=True):
  if pause_spotify:
    control_spotify('Pause')
  remove_control_file()
  create_control_file()
  p = subprocess.Popen(generate_play_command(file, idle=idle, mute=mute, video=video), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  pid = os.fork()
  if not pid:
    p.wait()
    remove_control_file()
    os._exit(0)

def get(prop):
  mpv = mpv_control()
  try:
    mpv.setup_socket(socketfile)
    result = mpv.get(prop)
    mpv.teardown_socket()
    return result
  except:
    mpv.teardown_socket()
    raise

def set(prop, value):
  mpv = mpv_control()
  mpv.setup_socket(socketfile)
  result = mpv.set(prop, value)
  mpv.teardown_socket()
  return result

def command(com):
  mpv = mpv_control()
  mpv.setup_socket(socketfile)
  mpv.command(com)
  mpv.teardown_socket()

if __name__ == '__main__':
  if len(sys.argv) > 2:
    if sys.argv[1] == 'play':
      play(sys.argv[2])
    elif sys.argv[1] == 'get':
      print(get(sys.argv[2]))
    elif sys.argv[1] == 'set':
      if len(sys.argv) > 3:
        set(sys.argv[2], sys.argv[3])
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'pause':
      command('cycle pause')
    elif sys.argv[1] == 'stop':
      command('stop')
    elif sys.argv[1] == 'next_chapter':
      command('add chapter 1')
    elif sys.argv[1] == 'prev_chapter':
      command('add chapter -1')
