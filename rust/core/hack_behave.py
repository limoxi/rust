# -*- coding: utf-8 -*-

"""
使得behave支持多个目录的feature加载
"""

from behave.runner import Runner

old_init_fn = Runner.__init__
def new_init_fn(self, config):
    old_init_fn(self, config)
    # self.config.paths.append('') todo

Runner.__init__ = new_init_fn