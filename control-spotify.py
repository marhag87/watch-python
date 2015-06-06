#!/usr/bin/env python

import dbus
import sys
import os

def control_spotify(command):
  os.environ['DISPLAY'] = ':0.0'
  session = dbus.SessionBus.get_session()
  spotify = session.get_object(
    "org.mpris.MediaPlayer2.spotify",
    "/org/mpris/MediaPlayer2")
  getattr(spotify, command)()

if __name__ == '__main__':
  if len(sys.argv) > 1:
    control_spotify(sys.argv[1])
