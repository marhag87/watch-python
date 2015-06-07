#!/usr/bin/env python3

import shutil
import os
import re

path = '/home/' + os.getlogin() + '/series/'

def move(file):
  if file.startswith(path):
    name = file.split('/')[-1]
    series = get_series(name)
    shutil.move(file, file.replace(path, path + series + '/'))

def get_series(filename):
  # Remove '.S10E22*'
  series = re.sub('\.*[sS]\d{2}[eE]\d{2}.*', '', filename)
  # Replace . and _ with ' '
  series = re.sub('[._]', ' ', series)
  # Remove year
  series = re.sub('\s*\d{4}\s*$', '', series)
  # Remove ' -*'
  series = re.sub('\s+-.+', '', series)
  # Remove '^[Translator] '
  series = re.sub('^\[.*?\]\s*', '', series)
  # Remove ' S2'
  series = re.sub('\s*[sS]\d{1}', '', series)
  # Remove ' 123 *'
  series = re.sub('\s*\d+.*', '', series)
  # Uppercase all words
  series = series.title()
  # Lowercase some words (A, X)
  series = re.sub('(\W)([AX])(\W)',
                  lambda m: m.group(1) +
                            m.group(2).lower() +
                            m.group(3),
                  series)
  # Lowercase after hyphen
  series = re.sub('(\w)(-)(\w)',
                  lambda m: m.group(1) +
                            m.group(2) +
                            m.group(3).lower(),
                  series)
  return series

def get_next_episode(filename, series):
  episodes = get_episodes(series)
  if episodes:
    episodes = list(episodes)
    episodes.sort()
    next = episodes.index(filename) + 1
    try:
      return episodes[next]
    except IndexError:
      return None

def get_episodes(series):
  for (_,_,filenames) in os.walk(path + series):
    return filenames

def link_next_episode(filename):
  series = get_series(filename)
  next_episode = get_next_episode(filename, series)
  if next_episode:
    if os.path.islink(path + series + '/next'):
      os.unlink(path + series + '/next')
    if next_episode != 'next':
      os.symlink(path + series + '/' + next_episode, path + series + '/next')
