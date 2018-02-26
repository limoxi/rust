#coding: utf8

from rust.command.base_command import BaseCommand

class Command(BaseCommand):

	def handle(self, *args):
		"""
		增加资源
		"""
		resource_name = args[1]