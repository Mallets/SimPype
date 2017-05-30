import simpype.pipe


class Priority(simpype.pipe.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)
		self.add_queue(id = 'express')
		self.add_queue(id = 'fast')
		self.add_queue(id = 'slow')
		self.add_queue(id = 'background')

	@simpype.pipe.dequeue
	def dequeue(self):
		if len(self.queue['express']) > 0:
			m = self.queue['express'].pop()
		elif len(self.queue['fast']) > 0:
			m = self.queue['fast'].pop()
		elif len(self.queue['slow']) > 0:
			m = self.queue['slow'].pop()
		else:
			m = self.queue['background'].pop()
		return m

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if 'priority' not in message.property:
			message.property['priority'] = 0

		if message.property['priority'].value == 3:
			m = self.queue['express'].push(message)
		elif message.property['priority'].value == 2:
			m = self.queue['fast'].push(message)
		elif message.property['priority'].value == 1:
			m = self.queue['slow'].push(message)
		elif message.property['priority'].value == 0:
			m = self.queue['background'].push(message)
		else:
			m = self.queue['background'].push(message)
		return m


# Do NOT remove
pipe = lambda *args: Priority(*args)
