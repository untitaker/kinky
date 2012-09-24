#!/usr/bin/env python3

import threading
import logging
from subprocess import Popen, PIPE

class StatusBar(object):
    before = ' '
    between = ' | '
    after = ' '
    items = None

    def __init__(self):
        self.items = []

    def run(self):
        for item in self.items:
            logging.debug('Spawning: ' + item.__class__.__name__)
            item.spawn(self)

    def draw(self):
        text = [item.text.replace('\n', '') for item in self.items if item.text is not None]
        text = self.between.join(text).strip()
        if text:
            print(self.before + text + self.after)

class Item(threading.Thread):
    thread = None
    bar = None
    running = None
    _text = None
    
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.bar.draw()

    def spawn(self, bar):
        self.bar = bar
        self.running = True
        self.start()

    def kill(self):
        self.running = False

    def run(self):
        raise NotImplementedError


# UTILS
def shell(command):
    '''Executes a command on the shell and returns its output'''
    return Popen(command, shell=True, stdout=PIPE).stdout.read().decode()

def is_running(process):
    '''Determines if a process with the given process name is running'''
    return shell('ps -A | grep -c ' + process).strip() != '0'
