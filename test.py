'''

Test use case

    $python test.py
    Success: 3
    Failure:
    - state: RETRY
    - ready: False
    - get: >> got exception: EngineTaskError Failed
    Zero: Done Normally
    Five: Done Rushed!
    $

'''
from subprocess import Popen

from engine import celery, tasks

pid = Popen(['celery', 'worker', '--app=engine', '-q'])

async_success = tasks.success.delay(1, 2)
async_failure = tasks.failure.delay()
async_zero = tasks.run_long.delay(0)
async_five = tasks.run_long.delay(5)

result = async_success.get()
print "********************************************"
print "Success:", result
print "Failure:"
print "- state:", async_failure.state
print "- ready:", async_failure.ready()
try:
    print "- get:", async_failure.get(timeout=3)
except StandardError as exc:
    print ">> got exception:", exc

print "********************************************"
print "Zero:", async_zero.get()
print "Five:", async_five.get()

pid.terminate()
print "********************************************"
print "Done!"
