import simpype.message
import simpype.pipe
import simpype.simulation


def __push(func, queue, message):
	assert isinstance(queue, Queue)
	assert isinstance(message, simpype.message.Message)
	message.queue = queue
	message.timestamp('pipe.'+str(queue.id)+'.in')
	result = func(queue, message)
	if isinstance(result, simpype.message.Message) and queue.active.triggered:
		queue.pipe.full()
	return result

def __pop(func, queue):
	assert isinstance(queue, Queue)
	message = func(queue)
	if isinstance(message, simpype.message.Message):
		message.timestamp('pipe.'+str(queue.id)+'.out')
		message.queue = None
	return message

def push(arg):
	if isinstance(arg, simpype.queue.Queue):
		queue = arg
		def decorator(func):
			def wrapper(queue, message):
				return __push(func, queue, message)
			queue.push = types.MethodType(wrapper, queue)
			return wrapper
		return decorator
	else:
		func = arg
		def wrapper(queue, message):
			return __push(func, queue, message)
		return wrapper

def pop(arg):
	if isinstance(arg, simpype.queue.Queue):
		queue = arg
		def decorator(func):
			def wrapper(queue):
				return __pop(func, queue)
			queue.pop = types.MethodType(wrapper, queue)
			return wrapper
		return decorator
	else:
		func = arg
		def wrapper(queue):
			return __pop(func, queue)
		return wrapper


class Queue:
	def __init__(self, sim, pipe, id):
		assert isinstance(sim, simpype.simulation.Simulation)
		assert isinstance(pipe, simpype.pipe.Pipe)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.pipe = pipe
		self.buffer = []
		self.capacity = float('inf')
		self.active = self.env.event().succeed()

	def _message_dropped(self, message, cause):
		assert isinstance(message, simpype.message.Message)
		assert message.queue == self
		if message in self.buffer:
			self.buffer.remove(message)
		message.timestamp('pipe.'+str(self.id)+'.'+str(cause))

	def enable(self):
		if not self.active.triggered:
			self.active.succeed()
		self.pipe.full()

	def disable(self):
		self.active = self.env.event()

	def __len__(self):
		return len(self.buffer)
