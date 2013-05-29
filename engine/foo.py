'''
General Useful Stuff with minimal celery-specific code


Really, only the SoftTimeLimitExceeded exception is needed so we can get
notified when our time is up when running long operations
'''
from __future__ import absolute_import
import time

from celery.exceptions import SoftTimeLimitExceeded


def success(x, y):
    return x + y


def failure(fail=True):
    if fail:
        raise Exception("Failed")


def handle_failure(name, exc):
    print "Task failed", name, exc


def run_long(seconds):
    try:
        # doing stuff
        time.sleep(seconds)
        return "Done Normally"
    except SoftTimeLimitExceeded:
        # hurry up and finish!
        return "Done Rushed!"
