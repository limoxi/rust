# coding: utf-8
__author__ = 'Asia'

class ConsoleBroker(object):

	def send(self, event):
		print (event.data)