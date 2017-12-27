import simpype


class Priority(simpype.pipe.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)
		self.add_queue(id = 'express')
		self.add_queue(id = 'fast')
		self.add_queue(id = 'slow')

	@simpype.pipe.dequeue
	def dequeue(self):
		if len(self.queue['express']) > 0:
			m = self.queue['express'].pop()
		elif len(self.queue['fast']) > 0:
			m = self.queue['fast'].pop()
		else:
			m = self.queue['slow'].pop()
		return m

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if message.id == 'first':
			m = self.queue['express'].push(message)
		elif message.id == 'business':
			m = self.queue['fast'].push(message)
		elif message.id == 'economy':
			m = self.queue['slow'].push(message)
		else:
			m = self.queue['slow'].push(message)
		return m


# Do NOT remove
pipe = lambda *args: Priority(*args)
