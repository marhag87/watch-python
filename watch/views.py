#!/usr/bin/env python3

import sys
sys.path.insert(0, 'scripts')

from django.shortcuts import render

from watch.shows import get_shows, get_episodes, get_next_episode, path
from scripts.play import play as mkvplay

def home(request):
  shows = get_shows()
  return render(request, 'home.html', {'shows': shows})

def show(request, myshow):
  episodes = get_episodes(myshow)
  next_episode = get_next_episode(myshow)
  return render(request, 'show.html', {'episodes': episodes, 'next_episode': next_episode, 'show': myshow})

def play(request, myshow, episode):
  mkvplay(path + myshow + '/' + episode)
  return show(request, myshow)
