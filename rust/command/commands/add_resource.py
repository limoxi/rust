
from rust.command.base_command import BaseCommand
from rust.utils.rust_cli_func import add_resource

class Command(BaseCommand):

	def handle(self, *args):
		"""
		增加资源
		"""
		resource_name = args[0]
		add_resource(resource_name)