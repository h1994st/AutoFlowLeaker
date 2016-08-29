#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-22 16:55:28
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from functools import wraps

from KThread import KThread


class TimeoutException(Exception):
    """function run timeout"""


def timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出TimeoutException异常"""

    def timeout_decorator(func):
        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        @wraps(func)
        def _(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get
            # the func return val to result list
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise TimeoutException(
                    'function run too long, timeout %d seconds.' % seconds)
            else:
                return result[0]
        return _
    return timeout_decorator
