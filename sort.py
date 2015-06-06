#!/usr/bin/env python3

import shutil
import os

def move(file):
  path = '/home/' + os.getlogin() + '/series/'
  if file.startswith(path):
    shutil.move(file, file.replace(path, path + 'Seen/'))
