'''
Sample Celery Abstraction Module
'''
from __future__ import absolute_import

from celery import Celery, Task
from celery.exceptions import RetryTaskError


celery = Celery('engine',
                broker='sqla+sqlite:///foo.db',
                backend='database',
                include=['engine.tasks'])

celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_RESULT_DBURI="sqlite:///foo.db",
    CELERY_DISABLE_RATE_LIMITS=True,
)


class AlwaysRetryTask(Task):  # pylint: disable=R0904
    '''Base of retrying tasks

    See: https://groups.google.com/forum/?fromgroups=#!topic/celery-users/
         DACXXud_8eI
    '''
    abstract = True
    default_retry_delay = 10
    max_retries = 2

    def __call__(self, *args, **kwargs):
        try:
            return self.run(*args, **kwargs)
        except RetryTaskError:
            raise   # task is already being retried.
        except Exception, exc:
            self.retry(exc=exc)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if einfo.internal is True:
            print "FAILED internally!", exc
        else:
            print "FAILED", exc
            celery.send_task("engine.tasks.handle_failure",
                             [self.__class__.__name__, exc])


if __name__ == '__main__':
    celery.start()
