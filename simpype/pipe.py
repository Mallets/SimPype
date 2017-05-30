import inspect
import simpy
import types

import simpype
import simpype.build


def __enqueue(func, pipe, message):
	assert isinstance(pipe, Pipe)
	assert isinstance(message, simpype.Message)
	message.location = pipe
	message.resource = pipe.resource
	if inspect.isgeneratorfunction(func):
		result = yield pipe.env.process(func(pipe, message))
	else:
		result = func(pipe, message)
	pipe.full()
	return result

def __dequeue(func, pipe):
	assert isinstance(pipe, Pipe)
	if inspect.isgeneratorfunction(func):
		result = yield pipe.env.process(func(pipe))
	else:
		result = func(pipe)
	return result

def enqueue(arg):
	if isinstance(arg, Pipe):
		pipe = arg
		def decorator(func):
			def wrapper(pipe, message):
				return __enqueue(func, pipe, message)
			pipe.enqueue = types.MethodType(wrapper, pipe)
			return wrapper
		return decorator
	else:
		func = arg
		def wrapper(pipe, message):
			return __enqueue(func, pipe, message)
		return wrapper

def dequeue(arg):
	if isinstance(arg, Pipe):
		pipe = arg
		def decorator(func):
			def wrapper(pipe):
				return __dequeue(func, pipe)
			pipe.dequeue = types.MethodType(wrapper, pipe)
			return wrapper
		return decorator
	else:
		func = arg
		def wrapper(pipe):
			return __dequeue(func, pipe)
		return wrapper


class Pipe:
	def __init__(self, sim, resource, id):
		assert isinstance(sim, simpype.Simulation)
		assert isinstance(resource, simpype.Resource)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.resource = resource
		self.available = self.env.event()
		self.queue = {}
		# Init
		self.a_wait_loop = self.env.process(self._wait_loop())

	def _message_dropped(self, message, cause):
		assert isinstance(message, simpype.Message)
		assert message.location == self

	def _wait_loop(self):
		while True:
			with self.resource.use.request() as request:
				yield request & self.available
				self.available = self.env.event()
				message = yield self.env.process(self.dequeue())
				if isinstance(message, simpype.Message):
					yield self.env.process(self.resource.service(message))
				self.full()

	def add_queue(self, id, model = None):
		queue = simpype.build.queue(self.sim, self, id, model)
		self.queue[queue.id] = queue
		return self.queue[queue.id]

	def full(self):
		tot = sum([len(q) for q in self.queue.values() if q.active.triggered])
		if not self.available.triggered and tot > 0:
			self.available.succeed()
