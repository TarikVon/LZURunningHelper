#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: util/module.py
#
# 用于兼容可选安装库
# 用于兼容标准库版本
#


__all__ = [
    "json",
    "JSONDecodeError",
    "random",
]


try:
    import simplejson as json
    from simplejson.errors import JSONDecodeError
except ModuleNotFoundError:
    import json
    from json.decoder import JSONDecodeError


import random

if not hasattr(random, "choices"):
    """random.choices 函数至少需要 python 3.6"""

    import itertools as _itertools
    import bisect as _bisect

    def choices(population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        if cum_weights is None:
            if weights is None:
                total = len(population)
                return [population[int(random.random() * total)] for i in range(k)]
            cum_weights = list(_itertools.accumulate(weights))
        elif weights is not None:
            raise TypeError("Cannot specify both weights and cumulative weights")
        if len(cum_weights) != len(population):
            raise ValueError("The number of weights does not match the population")
        total = cum_weights[-1]
        return [population[_bisect.bisect(cum_weights, random.random() * total)] for i in range(k)]

    random.choices = choices
