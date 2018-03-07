import simpype


class PriorityPreemption(simpype.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)		
		self.add_queue(id = 'preempted')
		self.add_queue(id = 'urgent')
		self.add_queue(id = 'normal')

	@simpype.pipe.dequeue
	def dequeue(self):
		if len(self.queue['urgent']) > 0:
			return self.queue['urgent'].pop()
		elif len(self.queue['preempted']) > 0:
			return self.queue['preempted'].pop()
		else:
			return self.queue['normal'].pop()

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if message.property['priority'].value == 'urgent':
			m = self.queue['urgent'].push(message)
			
			tlist = [t for t in self.resource.task.values() if t.process.is_alive and t.message.property['priority'].value != 'urgent']
			# If the resource is busy, preempt the current task
			if len(tlist) > 0:
				#task = max(tlist, key = lambda task: task.message.property['priority'].value)
				task = tlist[0]
				task.interrupt(cause = 'preempted')
				# This if is useful only in case of preemption with no restart
				if 'wait' in task.message.property:
					task.message.property['wait'] = task.message.property['wait'].value - (task.interrupted - task.started)
				self.queue['preempted'].push(task.message)
		else:
			m = self.queue['normal'].push(message)

		return m


# Do NOT remove
pipe = lambda *args: PriorityPreemption(*args)
