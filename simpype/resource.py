import inspect
import simpy
import types

import simpype.build
import simpype.message
import simpype.random
import simpype.simulation


def __service(func, resource, message):
	assert isinstance(resource, Resource)
	assert isinstance(message, simpype.message.Message)
	if inspect.isgeneratorfunction(func):
		mid = str(message.id)+str(message.seq_num)
		a_serve = resource.env.process(func(resource, message))
		resource.task[mid] = Task(message.sim, message, a_serve)
		try:
			yield a_serve
			message.timestamp('resource.serve')
		except simpy.Interrupt as interrupt:
			message.timestamp('resource.'+str(interrupt.cause))
		del resource.task[mid]
	else:
		func(resource, message)
		message.timestamp('resource.serve')
	if message.next:
		resource.send(message)
	else:
		message.done()


def service(arg):
	if isinstance(arg, simpype.resource.Resource):
		resource = arg
		def decorator(func):
			def wrapper(resource, message):
				return __service(func, resource, message)
			resource.service = types.MethodType(wrapper, resource)
			return wrapper
		return decorator
	else:
		func = arg
		def wrapper(resource, message):
			return __service(func, resource, message)
		return wrapper


class Task:
	def __init__(self, sim, message, process):
		assert isinstance(sim, simpype.simulation.Simulation)
		self.sim = sim
		self.env = sim.env
		self.message = message
		self.started = self.env.now
		self.interrupted = None
		self._process = process

	def interrupt(self, cause = None):
		self._process.interrupt(cause = cause)
		self.interrupted = self.env.now


class Resource:
	def __init__(self, sim, id, capacity = 1, pipe = None):
		assert isinstance(sim, simpype.simulation.Simulation)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.use = simpy.Resource(self.env, capacity = capacity)
		self.pipe = simpype.build.pipe(self.sim, self, self.id, pipe)
		self.random = simpype.random.RandomDict(self.sim)
		self.task = {}

	def _message_dropped(self, message, cause):
		mid = message.id+str(message.seq_num)
		assert mid in self.task
		self.task[mid].interrupt(cause = cause)

	def send(self, message):
		assert isinstance(message, simpype.message.Message)
		resource = list(message.next.values())
		for i in range(0, len(resource)):
			tmsg = message if i == (len(resource)-1) else message.copy()
			self.env.process(resource[i].pipe.enqueue(tmsg))
