import simpype


class PriorityPreemption(simpype.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)		
		self.add_queue(id = 'preempted')
		self.add_queue(id = 'express')
		self.add_queue(id = 'fast')
		self.add_queue(id = 'slow')

	@simpype.pipe.dequeue
	def dequeue(self):
		if len(self.queue['express']) > 0:
			return self.queue['express'].pop()
		elif len(self.queue['preempted']) > 0:
			return self.queue['preempted'].pop()
		elif len(self.queue['fast']) > 0:
			return self.queue['fast'].pop()
		else:
			return self.queue['slow'].pop()

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if 'priority' not in message.property:
			message.property['priority'] = 2

		if message.property['priority'].value == 0:
			m = self.queue['express'].push(message)
		elif message.property['priority'].value == 1:
			m = self.queue['fast'].push(message)
		elif message.property['priority'].value == 2:
			m = self.queue['slow'].push(message)
		else:
			m = self.queue['slow'].push(message)

		if isinstance(m, simpype.message.Message) and len(self.queue['express']) > 0:
			tlist = [t for t in self.resource.task.values() if t.process.is_alive and t.message.property['priority'].value != 0]
			if len(tlist) > 0:
				task = max(tlist, key = lambda task: task.message.property['priority'].value)
				task.interrupt(cause = 'preempted')
				task.message.property['wait'] = task.message.property['wait'].value - (task.interrupted - task.started)
				self.queue['preempted'].push(task.message)
		return m


# Do NOT remove
pipe = lambda *args: PriorityPreemption(*args)
