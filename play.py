#!/usr/bin/env python3

import sys
import os
import stat
import subprocess
from control_spotify import control_spotify
from mpv import mpv_control

socketfile = '/tmp/mpv_control'
help = 'Usage:\n' + \
       sys.argv[0] + ' <filename|web link>\n' + \
       sys.argv[0] + ' [play] <filename|web link>\n' + \
       sys.argv[0] + ' [pause]\n' + \
       sys.argv[0] + ' [stop]\n' + \
       sys.argv[0] + ' [get]  <property>\n' + \
       sys.argv[0] + ' [set]  <property> <value>'


def create_control_file():
  os.mkfifo(socketfile)

def remove_control_file():
  try:
    stat.S_ISFIFO(os.stat(socketfile).st_mode)
    os.remove(socketfile)
  except:
    pass

def generate_play_command(name, idle=False, mute=False, video=True):
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

def play(file, idle=False, mute=False, video=True, pause_spotify=True):
  if os.path.isfile(file) or file.startswith('http'):
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
  else:
    raise FileNotFoundError('Could not find file: ' + file)

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

def main(args=[]):
  if len(args) <= 1:
    print(help)
  if len(args) == 2:
    if   args[1] == 'pause':
      command('cycle pause')
    elif args[1] == 'stop':
      command('stop')
    elif args[1] == 'next_chapter':
      command('add chapter 1')
    elif args[1] == 'prev_chapter':
      command('add chapter -1')
    else:
      play(args[1])
  elif len(args) > 2:
    if   args[1] == 'play':
      play(args[2])
    elif args[1] == 'get':
      print(get(args[2]))
    elif args[1] == 'set':
      if len(args) > 3:
        set(args[2], args[3])

if __name__ == '__main__':
  main(sys.argv)
