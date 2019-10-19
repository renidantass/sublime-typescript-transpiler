import sublime, sublime_plugin
import subprocess
import os
import datetime

class Transpiler:
	def __init__(self, fn):
		self.__filename = fn
		self.__validate_file = None
		self.__path = "js"
		self.__returncode = 0
		self.status = None
		self.now = datetime.datetime.now()
		self.hour = self.now.strftime("%H:%M:%S")

	def __is_valid(self):
		if self.__filename.endswith('.ts'):
			return True
		else:
			return -1

	def __run(self):
		print(os.path.dirname(self.__filename))
		process = subprocess.Popen("tsc --p ../ts/", 
									stdout=subprocess.PIPE,
									shell=True)
		out, err = process.communicate()
		return (out.decode('ascii'), process.returncode)

	def __get_error (self, error):
		error = error[0]
		return error[:error.find(':')]

	def run(self):
		self.__validate_file = self.__is_valid()
		if self.__validate_file == True: 
			execution = self.__run()
			if ('error' not in execution[0]) and (execution[1] == 0):
				self.status = "✓ Transpilation sucessfully at {}".format(self.hour)
			else:
				self.status = "✗ Transpilation failed at {} - {}".format(self.hour, self.__get_error(execution))
		else:
			self.status = ""

class EventListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		transpiler = Transpiler(view.file_name())
		transpiler.run()
		view.set_status('transpiler', transpiler.status)