#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import threading

class myThread(threading.Thread):
	def __init__(self, thread_id):
		threading.Thread.__init__(self)

		self.id = thread_id
		self.counter = 0

	def run(self):
		while self.counter <= 100000:
			print('Thread: ' + str(self.id) + ': ' + str(self.counter))		
			self.counter += 1

thread_1 = myThread(1)
thread_2 = myThread(2)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
