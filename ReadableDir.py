#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-27 15:00:48
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import argparse


class ReadableDir(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(ReadableDir, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        prospectiveDir = values
        if not os.path.isdir(prospectiveDir):
            raise argparse.ArgumentTypeError(
                'readable directory:{0} is not a valid path'.format(
                    prospectiveDir))
        if os.access(prospectiveDir, os.R_OK):
            setattr(namespace, self.dest, os.path.abspath(prospectiveDir))
        else:
            raise argparse.ArgumentTypeError(
                'readable directory:{0} is not a readable dir'.format(
                    prospectiveDir))
