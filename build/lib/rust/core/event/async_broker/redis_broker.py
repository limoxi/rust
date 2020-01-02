# -*- coding: utf-8 -*-
__author__ = 'Asia'

class RedisBroker(object):

	def send(self, event):
		print event.data