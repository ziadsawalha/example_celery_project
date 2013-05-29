'''
Sample Celery Tasks Module

This module exposes functions from the project as celery tasks. It sets
values like retry delay and timeout. It can also catch, intercept, and redirect
exceptions
'''
from __future__ import absolute_import

from engine.celery import celery, AlwaysRetryTask
from engine import foo


class EngineTaskError(StandardError):
    '''An error that was raised in a task'''
    def __str__(self):
        return "EngineTaskError %s" % self.message


class InterruptedTaskError(StandardError):
    '''An error that was raised in a task by a keyboard or system interrupt'''
    def __str__(self):
        return "InterruptedTaskError %s" % self.message


@celery.task(base=AlwaysRetryTask, max_retries=0)
def success(x, y):
    return foo.success(x, y)


@celery.task(base=AlwaysRetryTask, default_retry_delay=2, max_retries=1)
def failure(fail=True):
    '''This task just demonstrates capturing errors from the called function
    and wrapping it in an exception that is application-specific. We could use
    this to attach certain context to certain error conditions (ex. is the
    error recoverable, resumeable, etc...)
    '''
    try:
        return foo.failure(fail=fail)
    except (KeyboardInterrupt, SystemExit) as exc:
        raise InterruptedTaskError(exc)
    except Exception as exc:
        raise EngineTaskError(exc)


@celery.task(base=AlwaysRetryTask)
def handle_failure(name, exc):
    return foo.handle_failure(name, exc)


@celery.task(base=AlwaysRetryTask, soft_time_limit=1)
def run_long(seconds):
    return foo.run_long(seconds)
