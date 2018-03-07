"""
SimPype's pipe.

"""
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
	""" Decorator for overloading the default :class:`Pipe` enqueue behavior.

	Args:
		arg (:class:`Pipe`)(``self``):
			The :class:`Pipe` instance.
			
	If the overloading is done in scripts, the :class:`Pipe` instance must be provided as decorator argument.
	
	.. code-block:: python

		myresource = sim.add_resource(id = 'myresource')
		myresource.add_queue(id = 'myqueue')

		@simpype.pipe.enqueue(myresource.pipe)
		def enqueue(self, message):
			return self.queue['myqueue'].push(message)

	If the overloading is done inside a Pipe subclass, the decorator must be called without any arguments. :class:`Pipe` instance is automatically provided through ``self``.

	.. code-block:: python
	   
		class MyPipe(simpype.Pipe):
			def __init__(self, sim, resource, id):
				super().__init__(sim, resource, id)
				self.add_queue(id = 'myqueue')

			@simpype.pipe.enqueue
			def enqueue(self, message):
				return self.queue['myqueue'].push(message)
	
	"""
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
	""" Decorator for overloading the default :class:`Pipe` dequeue behavior.

	Args:
		arg (:class:`Pipe`)(``self``):
			The :class:`Pipe` instance.
	
			
	If the overloading is done in scripts, the :class:`Pipe` instance must be provided as decorator argument.
	
	.. code-block:: python

		myresource = sim.add_resource(id = 'myresource')
		myresource.add_queue(id = 'myqueue')

		@simpype.pipe.dequeue(myresource.pipe)
		def dequeue(self):
			return self.queue['myqueue'].pop()

	If the overloading is done inside a Pipe subclass, the decorator must be called without any arguments. :class:`Pipe` instance is automatically provided through ``self``.

	.. code-block:: python
	   
		class MyPipe(simpype.Pipe):
			def __init__(self, sim, resource, id):
				super().__init__(sim, resource, id)
				self.add_queue(id = 'myqueue')

			@simpype.pipe.dequeue
			def dequeue(self):
				return self.queue['myqueue'].pop()

	"""	
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
	""" The pipe implements the queueing disciplines.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		resource (:class:`~simpype.resource.Resource`):
			The resource the pipe is associated to.
		id (str):
			The pipe id.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The pipe id.
		resource (:class:`~simpype.resource.Resource`):
			The resource the pipe is associated to.
		available (simpy.events.Event):
			Event signaling the presence of a :class:`~simpype.message.Message` in the pipe.
		queue (dict):
			The dictionary storing the :class:`~simpype.queue.Queue` instances associated to this pipe.

	"""
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
			yield self.resource.free & self.available
			self.available = self.env.event()
			if self.resource.free.triggered and \
				len(self.resource.task)+1 >= self.resource.capacity:
					self.resource.free = self.env.event()
			message = yield self.env.process(self.dequeue())
			if isinstance(message, simpype.Message):
				self.env.process(self._service(message))
			self.full()

	def _service(self, message):
		yield self.env.process(self.resource.service(message))
		if not self.resource.free.triggered and \
			len(self.resource.task) < self.resource.capacity:
				self.resource.free.succeed()


	def add_queue(self, id, model = None):
		""" Add a new queue to the pipe.

		Args:
			id (str):
				The id of the new queue.
			model (str):
				The model of the new queue. If model is ``None``, the default queue model is created.

		Returns:
			:class:`~simpype.queue.Queue`

		"""
		queue = simpype.build.queue(self.sim, self, id, model)
		self.queue[queue.id] = queue
		return self.queue[queue.id]

	def full(self):
		""" Check if there is at least a :class:`~simpype.message.Message` in the pipe.

		Returns:
			bool

		"""
		tot = sum([len(q) for q in self.queue.values() if q.active.triggered])
		if not self.available.triggered and tot > 0:
			self.available.succeed()
			return True
		return False
