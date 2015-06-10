#!/usr/bin/env python3

import os

path = '/storage/series/'

def get_shows():
  for (_,dirs,_) in os.walk(path):
    shows = list(dirs)
    shows.sort()
    try:
      shows.remove('Finished')
      shows.remove('Seen')
      shows.remove('Crap')
      shows.remove('Maybe later')
    except ValueError:
      pass
    return shows

def get_episodes(show):
  for (_,_,files) in os.walk(path + show):
    episodes = list(files)
    episodes = sorted(episodes, key=lambda s: s.lower())
    try:
      episodes.remove('next')
    except ValueError:
      pass
    return episodes

def get_next_episode(show):
  next_episode = os.path.realpath(path + show + '/next')
  if os.path.isfile(next_episode):
    return next_episode.split('/')[-1]
