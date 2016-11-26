#!/usr/bin/env python3

import time
import threading
import logging
import subprocess


class StatusBar(object):
    before = ' '
    between = ' | '
    after = ' '
    error_value = 'restarting'
    items = None

    def __init__(self):
        self.items = []

    def run(self):
        for item in self.items:
            logging.debug('Spawning: ' + item.__class__.__name__)
            item.spawn(self)

    def draw(self):
        text = [item.text.replace('\n', '')
                for item in self.items if item.text is not None]
        text = self.between.join(text).strip()
        if text:
            print(self.before + text + self.after)


class Item(object):
    _thread = None
    bar = None
    _text = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value == self._text:
            return
        self._text = value
        self.bar.draw()

    def spawn(self, bar):
        self.bar = bar
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        while True:
            try:
                self.run()
            except Exception:
                logging.exception('')
                self.text = self.bar.error_value
                time.sleep(5)
            else:
                self.text = None
                break

    def run(self):
        raise NotImplementedError()


# UTILS

def shell_stream(command):
    '''Stream lines of command stdout'''
    p = subprocess.Popen(command, shell=True, universal_newlines=True,
                         stdout=subprocess.PIPE)
    yield from p.stdout


def shell(command, errors=False):
    '''Executes a command on the shell and returns its output'''
    try:
        return subprocess.check_output(command, shell=True) \
                .decode('utf-8', errors='replace')
    except subprocess.CalledProcessError:
        if errors:
            raise

def is_running(process):
    '''Determines if a process with the given process name is running'''
    return shell('ps -A | grep -q ' + process) is not None
