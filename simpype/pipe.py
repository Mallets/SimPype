import inspect
import simpy

import simpype.build
import simpype.resource
import simpype.simulation


# Pipe decorator
def enqueue(f):
	def wrapper(pipe, message):
		assert isinstance(pipe, Pipe)
		assert isinstance(message, simpype.message.Message)
		message.resource = pipe.resource
		if inspect.isgeneratorfunction(f):
			result = yield pipe.env.process(f(pipe, message))
		else:
			result = f(pipe, message)
		pipe.full()
		return result
	return wrapper


def dequeue(f):
	def wrapper(pipe):
		assert isinstance(pipe, Pipe)
		if inspect.isgeneratorfunction(f):
			result = yield pipe.env.process(f(pipe))
		else:
			result = f(pipe)
		return result
	return wrapper


class Pipe:
	def __init__(self, sim, resource, id):
		assert isinstance(sim, simpype.simulation.Simulation)
		assert isinstance(resource, simpype.resource.Resource)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.resource = resource
		self.available = self.env.event()
		self.queue = {}
		# Init
		self.a_wait_loop = self.env.process(self._wait_loop())

	def _wait_loop(self):
		while True:
			with self.resource.use.request() as request:
				yield request & self.available
				self.available = self.env.event()
				message = yield self.env.process(self.dequeue())
				if isinstance(message, simpype.message.Message):
					yield self.env.process(self.resource.service(message))
				self.full()

	def add_queue(self, id, model = None):
		queue = simpype.build.queue(self.sim, self, id, model)
		self.queue[queue.id] = queue
		return self.queue[queue.id]

	def full(self):
		if not self.available.triggered and \
		sum([len(q) for q in self.queue.values() if q.active.triggered]) > 0:
			self.available.succeed()
