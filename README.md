## Sample Celery Project

Clone it. Have celery and sqlite installed. Run `test.py`.

    $python test.py
    Success: 3
    Failure:
    - state: RETRY
    - ready: False
    - get: >> got exception: EngineTaskError Failed
    Zero: Done Normally
    Five: Done Rushed!
    $

## Demonstrates

Things I wish I had known when I first started using celery...

1. Minimal startup of celery (no rabbitmq)
2. Starting celery from inside my main app process
3. Setting up your project with a [Dedicated Module](http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#project-layout)
4. Keeping celery code separate from your logic with [custom tasks](https://groups.google.com/d/msg/celery-users/DACXXud_8eI/uB4J_xryR5wJ)
5. Gently interrupting long-running tasks using [soft limits](http://docs.celeryproject.org/en/latest/userguide/tasks.html#Task.soft_time_limit)
6. [Capturing errors](http://docs.celeryproject.org/en/latest/userguide/tasks.html#on_failure) and routing them for special/central handling
