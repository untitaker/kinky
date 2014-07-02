=====
Kinky
=====

Simple toolkit for custom conky-cli-like statusbar scripts, written in Python 3. 

Usage
=====

Create a file called `my_kinky.py`:

.. code-block:: python

    import os
    import datetime
    import time
    from kinky import Item, StatusBar

    class Clock(Item):
        def run(self):
            while True:
                self.text = datetime.datetime.now().strftime('%H:%M')
                time.sleep(60)  # update interval: a minute

    class Volume(Item):
        def run(self):
            while True:
                # somehow get system volume and save it as a string in self.text
                # self.text = "34%"
                time.sleep(.3)  # update interval: 0.3 seconds

    statusbar = StatusBar()
    statusbar.items = [Volume(),Clock()]
    statusbar.between = '; '
    statusbar.run()


Every time an item writes to its text attribute, the statusbar will write a new
line. Running this from the command line gives us::

    $ python3 my_kinky.py

    34%; 20:15
    34%; 20:16
    34%; 20:17

... because the Volume doesn't change, but the Clock triggers an update every minute.

This is intended for usage with dzen2::

    python -u mystatusbar.py | dzen2  # -u disables stdout buffering

::

License
=======

Kinky is released under the public domain.
