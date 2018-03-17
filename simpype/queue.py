"""
SimPype's queue.

"""
import types

import simpype


def __push(func, queue, message):
	assert isinstance(queue, simpype.Queue)
	assert isinstance(message, simpype.Message)
	message.location = queue
	message.timestamp('pipe.in')
	result = func(queue, message)
	if isinstance(result, simpype.Message) and queue.active.triggered:
		queue.pipe.full()
	return result

def __pop(func, queue):
	assert isinstance(queue, Queue)
	message = func(queue)
	if isinstance(message, simpype.Message):
		message.timestamp('pipe.out')
		message.queue = None
	return message

def push(arg):
	""" Decorator for overloading the default :class:`Queue` push behavior.

	Args:
		arg (:class:`Queue`)(``self``):
			The :class:`Queue` instance.
			
	If the overloading is done in scripts, the :class:`Queue` instance must be provided as decorator argument.
	
	.. code-block:: python

		myresource = sim.add_resource(id = 'myresource')
		myresource.add_queue(id = 'myqueue')

		@simpype.queue.push(myresource.pipe['myqueue'])
		def push(self, message):
			self.buffer.append(message)
			return message

	If the overloading is done inside a Queue subclass, the decorator must be called without any arguments. :class:`Queue` instance is automatically provided through ``self``.

	.. code-block:: python
	   
		class MyQueue(simpype.Queue):
			def __init__(self, sim, pipe, id):
				super().__init__(sim, pipe, id)

			@simpype.queue.push
			def push(self, message):
				self.buffer.append(message)
				return message
	
	"""
	if isinstance(arg, simpype.Queue):
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
	""" Decorator for overloading the default :class:`Queue` pop behavior.

	Args:
		arg (:class:`Queue`)(``self``):
			The :class:`Queue` instance.
			
	If the overloading is done in scripts, the :class:`Queue` instance must be provided as decorator argument.
	
	.. code-block:: python

		myresource = sim.add_resource(id = 'myresource')
		myresource.add_queue(id = 'myqueue')

		@simpype.queue.pop(myresource.pipe['myqueue'])
		def pop(self):
			return self.buffer.pop(0)

	If the overloading is done inside a Queue subclass, the decorator must be called without any arguments. :class:`Queue` instance is automatically provided through ``self``.

	.. code-block:: python
	   
		class MyQueue(simpype.Queue):
			def __init__(self, sim, pipe, id):
				super().__init__(sim, pipe, id)

			@simpype.queue.pop
			def pop(self):
				return self.buffer.pop(0)
	
	"""
	if isinstance(arg, simpype.Queue):
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
	""" Queue is used by :class:`~simpype.pipe.Pipe` to store :class:`~simpype.message.Message` objects.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		pipe (:class:`~simpype.pipe.Pipe`):
			The pipe this queue is associated to.
		id (str):
			The queue id.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The queue id.
		pipe (:class:`~simpype.pipe.Pipe`):
			The pipe this queue is associated to.
		buffer (list):
			The data structure physically storing the :class:`~simpype.message.Message` objects.
		capacity (int):
			The capacity of the buffer. ``Infinite`` by default.
		active (simpy.events.Event):
			Event signaling when the queue is active.

	"""
	def __init__(self, sim, pipe, id):
		assert isinstance(sim, simpype.Simulation)
		assert isinstance(pipe, simpype.Pipe)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.pipe = pipe
		self.buffer = []
		self.capacity = float('inf')
		self.log = True
		self.active = self.env.event().succeed()

	@property
	def log(self):
		return self._log

	@log.setter
	def log(self, value):
		assert isinstance(value, bool)
		self._log = value

	def _message_dropped(self, message, cause):
		assert isinstance(message, simpype.Message)
		assert message.location == self
		if message in self.buffer:
			self.buffer.remove(message)
		message.timestamp('pipe.'+str(self.id)+'.'+str(cause))

	def enable(self):
		""" Enable this queue by triggering the ``active`` attribute. """
		if not self.active.triggered:
			self.active.succeed()
		self.pipe.full()

	def disable(self):
		""" Disable this queue by resetting the ``active`` attribute. """
		self.active = self.env.event()

	def __len__(self):
		return len(self.buffer)
