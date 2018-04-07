#!/usr/bin/env python2

# Based on this gist https://gist.github.com/n1ywb/2570004
# by Jeff Laughlin Consulting LLC
#
# May 1, 2012           Initial version by Jeff Laughlin Consulting LLC
# December 11, 2017     Modified version by Konstantinos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time


def retry_exc_handler(tries_remaining, exception, delay):
    """
    Exception handler for the retry decorator, logs exceptions to the database
    :param tries_remaining: The number of tries remaining
    :param exception: The exception instance which was raised
    :param delay: We will sleep this many seconds
    """

    print 'Caught \'{0}\', {1} tries remaining, sleeping for {2} seconds'.format(exception, tries_remaining, delay)


def retries(max_tries, delay=1, backoff=2, exceptions=(Exception,), hook=None):
    """
    Function decorator implementing retrying logic
    Based on: https://gist.github.com/n1ywb/2570004

    The decorator will call the function up to max_tries times if it raises
    an exception.

    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify
    a custom tuple of exception classes with the `exceptions` argument; the
    function will only be retried if it raises one of the specified exceptions.

    Additionally, you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance.
    This is primarily intended to give the opportunity to log the failure.
    Hook is not called after failure if no retries remain.
    
    :param max_tries: The decorator will call the function up to max_tries time
    :param delay: Sleep this many seconds * backoff * try number after failure
    :param backoff: Multiple delay by this factor after each failure
    :param exceptions: A tuple of exception classes; default (Exception,)
    :param hook: A function with the signature myhook(tries_remaining, exception, delay);
                 default None
    """

    def dec(func):
        def f2(*args, **kwargs):
            my_delay = delay
            tries = range(max_tries)
            tries.reverse()

            for tries_remaining in tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, my_delay)
                        time.sleep(my_delay)
                        my_delay *= backoff
                    else:
                        raise
                # else:
                #     break
        return f2
    return dec
