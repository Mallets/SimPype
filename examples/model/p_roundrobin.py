import simpype.pipe


class RoundRobin(simpype.pipe.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)
		for i in range(0,4):
			self.add_queue(id = i)
		self.last = 3

	@simpype.pipe.dequeue
	def dequeue(self):
		# The priority policy
		for i in range(0, len(self.queue)):
			self.last = (self.last + 1) % len(self.queue)
			if len(self.queue[self.last]) > 0:
				break
		return self.queue[self.last].pop()

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if 'priority' not in message.property:
			message.property['priority'] = 0

		if message.property['priority'].value == 3:
			m = self.queue[3].push(message)
		elif message.property['priority'].value == 2:
			m = self.queue[2].push(message)
		elif message.property['priority'].value == 1:
			m = self.queue[1].push(message)
		elif message.property['priority'].value == 0:
			m = self.queue[0].push(message)
		else:
			m = self.queue[0].push(message)

		return self.queue[priority].push(message)


# Do NOT remove
pipe = lambda *args: RoundRobin(*args)
