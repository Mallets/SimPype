import simpype


class Pipe(simpype.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)
		self.add_queue(id = 'default')

	@simpype.pipe.dequeue
	def dequeue(self):
		return self.queue['default'].pop()
						        
	@simpype.pipe.enqueue
	def enqueue(self, message):
		return self.queue['default'].push(message)
															

# Do NOT remove
pipe = lambda *args: Pipe(*args)
