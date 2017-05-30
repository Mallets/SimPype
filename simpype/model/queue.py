import simpype


class Queue(simpype.Queue):
	def __init__(self, sim, pipe, id):
		super().__init__(sim, pipe, id)

	@simpype.queue.push
	def push(self, message):
		assert isinstance(message, simpype.Message)
		if len(self.buffer) < self.capacity:
			self.buffer.append(message)
			return message
		else:
			message.drop('full')
			return None

	@simpype.queue.pop
	def pop(self):
		if len(self.buffer) > 0:
			return self.buffer.pop(0)
		else:
			return None

# Do NOT remove
queue = lambda *args: Queue(*args)
