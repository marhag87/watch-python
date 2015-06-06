#!/usr/bin/env python3

import shutil
import os
import re

path = '/home/' + os.getlogin() + '/series/'

def move(file):
  if file.startswith(path):
    shutil.move(file, file.replace(path, path + 'Seen/'))

def sort_seen(file):
  if file.startswith(path + 'Seen/'):
    name = file.split('/')[-1]
    series = re.split('\d', name)[0]
    target = path + series + '/' + name
    shutil.move(file, target)
