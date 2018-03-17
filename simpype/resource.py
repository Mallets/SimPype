"""
SimPype's resources process :class:`~simpype.message.Message` objects.
The behavior of each resource can be customized by overloading the custom
``service`` function through the decorator ``@simpype.resource.service``.
See :ref:`resource` :func:`service` for more details on how to customize a :class:`Resource` behavior.

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['wait'] = {
       0: lambda: random.uniform(0,1)
   }
   res0 = sim.add_resource(id = 'res0')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   @simpype.resource.service(res0)
   def service(self, message):
       # Wait for a random time
       yield self.env.timeout(self.random['service'])
       # Wait for a time as reported in the message property
       yield self.env.timeout(message.property['wait'].value)

   sim.run(until = 10)

"""
import inspect
import simpy
import types

import simpype
import simpype.build


def __service(func, resource, message):
	assert isinstance(resource, Resource)
	assert isinstance(message, simpype.Message)
	message.location = resource
	if inspect.isgeneratorfunction(func):
		a_serve = resource.env.process(func(resource, message))
		task = resource.add_task(message, a_serve)
		try:
			yield a_serve
			message.timestamp('resource.serve')
		except simpy.Interrupt as interrupt:
			message.timestamp('resource.'+str(interrupt.cause))
		resource.del_task(task)
	else:
		func(resource, message)
		message.timestamp('resource.serve')
	if message.next:
		resource.send(message)
	else:
		message.done()


def service(arg):
	""" Decorator for overloading the default :class:`Resource` service behavior.


	Args:
		arg (:class:`Resource`)(``self``):
			The :class:`Resource` instance.
	
			
	If the overloading is done in scripts, the :class:`Resource` instance must be provided as decorator argument.
	
	.. code-block:: python

		myresource = sim.add_resource(id = 'myresource1')

		@simpype.resource.service(myresource)
		def service(self, message):
			yield self.env.timeout(1.0)

	If the overloading is done inside a Resource subclass, the decorator must be called without any arguments. :class:`Resource` instance is automatically provided through ``self``.

	.. code-block:: python
	   
		class MyResource(simpype.Resource):
			def __init__(self, sim, id, capacity = 1, pipe = None):
				super().__init__(sim, id, capacity, pipe)

			@simpype.resource.service
			def service(self, message):
				yield self.env.timeout(1.0)
	
	"""
	if isinstance(arg, simpype.Resource):
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
	""" This class implements the :class:`Task` managed by the :class:`Resource`.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		message (:class:`~simpype.message.Message`):
			The message being processed in this class
		process (simpy.events.Process):
			The SimPy process to execute

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		message (:class:`~simpype.message.Message`):
			The message being processed in this class
		started (float):
			The simulation time this task was started
		interrupted (float):
			The simulation time this task was interrupted. ``None`` if active.
		process (simpy.events.Process):
			The SimPy process being executed

	"""
	def __init__(self, sim, message, process):
		assert isinstance(sim, simpype.Simulation)
		assert isinstance(message, simpype.Message)
		self.id = str(message.id)+str(message.seq_num)
		self.sim = sim
		self.env = sim.env
		self.message = message
		self.started = self.env.now
		self.interrupted = None
		self.process = process

	def interrupt(self, cause = None):
		self.process.interrupt(cause = cause)
		self.interrupted = self.env.now


class Resource:
	""" This class implements the :class:`Resource` object.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		id (str):
			The resource id.
		capacity (int):
			The simpy.Resource capacity.
		pipe (:class:`Pipe`):
			The SimPype pipe model associated to this resource.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The simpype.Resource id.
		use (simpy.Resource):
			The SimPy resource object.
		pipe (:class:`Pipe`):
			The SimPype pipe object.
		random (:class:`RandomDict`):
			The SimPype RandomDict object.
		task (dict):
			The dictionary storing the task currenty being executed by the resource.

	"""
	def __init__(self, sim, id, capacity = 1, pipe = None):
		assert isinstance(sim, simpype.Simulation)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.capacity = capacity
		self.available = self.env.event().succeed()
		self.pipe = simpype.build.pipe(self.sim, self, self.id, pipe)
		self.random = simpype.random.RandomDict(self.sim)
		self.task = {}
		self.log = True

	@property
	def log(self):
		return self._log

	@log.setter
	def log(self, value):
		assert isinstance(value, bool)
		self._log = value
		self.pipe.log = value

	def _message_dropped(self, message, cause):
		assert isinstance(message, simpype.Message)
		assert message.location == self
		tid = str(message.id)+str(message.seq_num)
		assert tid in self.task
		self.task[tid].interrupt(cause = cause)

	def free(self):
		if self.available.triggered:
			if len(self.task)+1 >= self.capacity:
				self.available = self.env.event()
		else:
			if len(self.task) < self.capacity:
				self.available.succeed()

	def add_task(self, message, process):
		t = Task(self.sim, message, process)
		self.task[t.id] = t
		return t

	def del_task(self, task):
		assert task.id in self.task
		del self.task[task.id]

	def send(self, message):
		""" Send a :class:`~simpype.message.Message`.

		Args:
			message (:class:`~simpype.message.Message`):
				The message to send.

		"""
		assert isinstance(message, simpype.Message)
		resource = list(message.next.values())
		for i in range(0, len(resource)):
			tmsg = message if i == (len(resource)-1) else message.copy()
			self.env.process(resource[i].pipe.enqueue(tmsg))
