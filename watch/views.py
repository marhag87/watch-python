#!/usr/bin/env python3

from django.shortcuts import render

from watch.shows import get_shows, get_episodes, get_next_episode

def home(request):
  shows = get_shows()
  return render(request, 'home.html', {'shows': shows})

def show(request, show):
  episodes = get_episodes(show)
  next_episode = get_next_episode(show)
  return render(request, 'show.html', {'episodes': episodes, 'next_episode': next_episode, 'show': show})
