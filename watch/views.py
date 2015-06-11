#!/usr/bin/env python3

import sys
sys.path.insert(0, 'scripts')

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from watch.shows import get_shows, get_episodes, get_next_episode, path
from scripts.play import play as mkvplay
from scripts.play import command as mkvcommand

def home(request):
  shows = get_shows()
  return render(request, 'home.html', {'shows': shows})

def show(request, myshow):
  episodes = get_episodes(myshow)
  next_episode = get_next_episode(myshow)
  return render(request, 'show.html', {'episodes': episodes, 'next_episode': next_episode, 'show': myshow})

def play(request, myshow, episode):
  mkvplay(path + myshow + '/' + episode)
  return redirect('/show/' + myshow)

def command(request, cmd):
  if cmd == 'pause':
    mkvcommand('cycle pause')
    return HttpResponse('')
  if cmd == 'stop':
    mkvcommand('stop')
    return HttpResponse('')
  if cmd == 'nextchapter':
    mkvcommand('add chapter 1')
    return HttpResponse('')
  if cmd == 'prevchapter':
    mkvcommand('add chapter -1')
    return HttpResponse('')
  else:
    return HttpResponseBadRequest('Invalid command')
