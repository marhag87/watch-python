#!/usr/bin/env python3

import socket
import json
import sys

class mpv_control():

  def setup_socket(self, mysocket):
    self.mpv_socket = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    self.mpv_socket.settimeout(0.5)
    try:
      self.mpv_socket.connect(mysocket)
    except ConnectionRefusedError:
      raise
    except FileNotFoundError:
      raise

  def teardown_socket(self):
    self.mpv_socket.close()

  def mpv_command(self, cmd):
    self.mpv_socket.send(cmd.encode())
    try:
      ret = self.mpv_socket.recv(4096).decode()
    except socket.timeout:
      return
    j = json.loads(ret.split('\n')[0])
    if j.get('error') == 'success' or j.get('error') == None:
      return(j.get('data'))
    else:
      return(j.get('error'))

  def get(self, property):
    return self.mpv_command(''.join([json.dumps({'command': ['get_property', property]}), '\n']))

  def set(self, property, value):
    return self.mpv_command(''.join([json.dumps({'command': ['set_property_string', property, value]}), '\n']))

  def json_command(self, command):
    return self.mpv_command(''.join([json.dumps({'command': command}), '\n']))

  def command(self, com):
    self.mpv_command(com + '\n')
