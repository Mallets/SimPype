"""
SimPype's message.

"""

import copy
import inspect
import simpy

import simpype
import simpype.build


class PropertyDict(dict):
	""" A custom dictionary storing simpype.Property objects.
	
	Args:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object

	Attributes:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		env (simpy.Environment): 
			The SimPy environment object

	"""
	def __init__(self, sim):
		assert isinstance(sim, simpype.Simulation)
		super().__init__()
		self.sim = sim
		self.env = sim.env
	
	def __setitem__(self, key, value):
		""" Automatically creates a simpype.Property object when assigning a value

		Args:
			key (any):
				The dictionary key
			value (any):
				The dictionaty value

		"""
		# Don't create a simpype.Property object if value is already a simpype.Property object
		if isinstance(value, Property):
			super().__setitem__(key, value)
		else:
			super().__setitem__(key, Property(self.sim, key, value))


class Property:
	""" This class implements the properties used by simpype.Message objects.
	
	A property value can be either static or dynamic. In the latter case
	the ``value`` must follow the simpype.Random value dictionary format.

	Args:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		name (str):
			The property name
		value (any):
			The property value

	Attributes:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		env (simpy.Environment):
			The SimPy environment object
		name (str):
			The property name
		value (any):
			The property value

	"""
	def __init__(self, sim, name, value):
		assert isinstance(sim, simpype.Simulation)
		self.sim = sim
		self.env = sim.env
		self.name = name
		# If ``value`` is a dictionary and contains lambda functions, create a simpype.Random object
		if isinstance(value, dict) and [f for f in value.values() if inspect.isfunction(f)]:
			self._random = simpype.Random(self.sim, value)
			self._value = self._random.value
		else:
			self._random = None
			self._value = value

	@property
	def value(self):
		""" The value of the simpype.Property. """
		return self._value

	def copy(self):
		""" Create a copy of the object.

		Returns:
			:class:`Property`
		"""
		property = Property(self.sim, self.name, self._value)
		property._random = self._random
		return property

	def refresh(self):
		""" Generate a new random value for the simpype.Property object. 
		
		This function does not produce any effects if the simpype.Property value is static.

		"""
		if isinstance(self._random, simpype.Random):
			self._value = self._random.value


class Timestamp:
	""" This class implements the timestamps used by simpype.Message objects.

	Timestamp objects are used for logging purposes.

	Args:
		message (:class:`Message`):
			The SimPype message object this timestamp is associated to
		timestamp (int,float):
			The simulation time of the timestmap
		resource (:class:`~simpype.resource.Resource`):
			The SimPype resource object creating the timestamp
		description (str):
			The description of the event generating the timestamp

	Attributes:
		message (:class:`Message`):
			The SimPype message object this timestamp is associated to
		timestamp (int,float):
			The simulation time of the timestmap
		resource (:class:`~simpype.resource.Resource`):
			The SimPype resource object creating the timestamp
		description (str):
			The description of the event generating the timestamp

	"""
	def __init__(self, message, timestamp, resource, description):
		assert isinstance(message, Message)
		assert isinstance(resource, simpype.Resource)
		self.message = message
		self.timestamp = float(timestamp)
		self.resource = resource
		self.description = str(description)


class Subscription:
	""" This class implements the subscriptions used by simpype.Message objects.

	Subscription used to execute a given function upong some events triggering.

	Args:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		message (:class:`Message`):
			The SimPype message object this timestamp is associated to
		event (simpy.Event):
			The Simpy event the simpype.Message object is subscribed to
		callback (user-defined python function):
			The python function to call upon event triggering
		id (str):
			The simpype.Subscription id

	Attributes:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		env (simpy.Environment):
			The SimPy environment object
		message (:class:`~simpype.message.Message`):
			The SimPype message object this timestamp is associated to
		event (simpy.Event):
			The Simpy event the simpype.Message object is subscribed to
		callback (user-defined python function):
			The python function to call upon event triggering
		id (str):
			The simpype.Subscription id
		disable (simpy.Event):
			The Simpy event used to remove the subscription

	"""
	def __init__(self, sim, message, event, callback, id):
		assert isinstance(sim, simpype.Simulation)
		assert isinstance(message, Message)
		assert callable(callback)
		self.sim = sim
		self.env = sim.env
		self.message = message
		self.event = event
		self.callback = callback
		self.id = id
		self.disable = self.env.event()


class Message:
	""" This class implements the simpype.Message object.

	simpype.Message object is the atomic unit processed by simpype.Resource objects.

	Args:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object
		resource (:class:`~simpype.resource.Resource`):
			The simpype.Resource object generating this message
		id (str):
			The SimPype message id

	Attributes:
		sim (:class:`~simpype.simulation.Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The simpype.Message id
		generated (float):
			The simulation time when this object was generated.
		generator (:class:`~simpype.resource.Resource`):
			The simpype.Resource that created the message.
		is_alive (bool):
			The boolean value marking if the message is alive or not. 
			A message is not alive when no further steps are available or if it is used as a template by a generator.
		location (:class:`~simpype.resource.Resource`:class:`~simpype.pipe.Pipe`:class:`~simpype.queue.Queue`):
			The location of the simpype.Message inside the simulation pipeline.
		property (:class:`PropertyDict`): 
			The PropertyDict dictionary storing the :class:`Property` objects
		seq_num (int):
			The sequence number of the message
		subscription (dict):
			The dictionary storing the Subscription objects
		visited (list):
			The list of the visited simpype.Resource objects

	"""
	def __init__(self, sim, resource, id):
		assert isinstance(sim, simpype.Simulation)
		assert isinstance(resource, simpype.Resource)
		self.sim = sim					
		self.env = sim.env
		self.id = id
		self.generated = self.env.now
		self.generator = resource
		self.is_alive = True
		self.log = True
		self.location = resource
		self.property = PropertyDict(self.sim)
		self.seq_num = 0
		self.subscription = {}
		self.visited = []
		self.next = {}
		self.resource = resource
		self.pipeline = simpype.Pipeline(self.sim, self.id)

	@property
	def next(self):
		""" The next resources available to the message in the form of adjency list 

		Next property admits only simpype.Resource, simpype.Pipeline, and next-compatible values

		"""
		return self._next
	
	@next.setter
	def next(self, value):
		assert isinstance(value, (simpype.Resource, simpype.Pipeline, dict))
		if isinstance(value, simpype.Resource):
			self._next = {value.id: value}
		elif isinstance(value, simpype.Pipeline):
			self._next = {value.first.id: value.first}
		elif isinstance(value, dict):
			self._next = value

	@property
	def pipeline(self):
		""" The pipeline associated to the message in the form of adjency.

		A pipeline represents all the possible paths to the message.
		Pipeline property admits only simpype.Pipeline objects as a value

		"""
		return self._pipeline
	
	@pipeline.setter
	def pipeline(self, value):
		assert isinstance(value, simpype.Pipeline)
		self._pipeline = value
		if hasattr(self, 'resource'):
			self._update_next()

	@property
	def resource(self):
		""" The resource currently managing the message.

		Resource property admits only simpype.Resource objects as a value

		"""
		return self._resource
	
	@resource.setter
	def resource(self, value):
		assert isinstance(value, simpype.Resource)
		self._resource = value
		self.visited.append(value)
		if hasattr(self, 'pipeline'):
			self._update_next()

	def _drop(self, message, cause):
		""" The callback function fro dropping a message """
		self.done()
		self.location._message_dropped(self, cause)

	def _update_next(self):
		""" Update the next adjency list based on the current resource managing the message """
		if self.resource.id in self.pipeline.resource:
			self.next = {p.id: p for p in self.pipeline.resource[self.resource.id]}
		else:
			self.next = {}

	def _wait_event(self, subscription):
		""" Wait the triggering of an event and execute the associated callbak """
		value = yield subscription.event | subscription.disable
		if subscription.event in value and self.is_alive:
			subscription.callback(self, value[subscription.event])
		if subscription.id in self.subscription:
			del self.subscription[subscription.id]
	
	def copy(self):
		""" Create a dopy of this simpype.Message object. 
		
		Returns:
			:class:`Message`

		"""
		message = Message(self.sim, self.generator, self.id)
		message.generated = copy.deepcopy(self.generated)
		message.resource = self.resource
		message.location = self.location
		message.seq_num = copy.deepcopy(self.seq_num)
		message.visited = copy.copy(self.visited)
		message.is_alive = copy.deepcopy(self.is_alive)
		message.log = copy.deepcopy(self.log)
		message.next = copy.copy(self.next)
		message.pipeline = copy.copy(self.pipeline)
		for p in self.property.values():
			message.property[p.name] = p.copy()
		for id,s in self.subscription.items():
			c = getattr(message, s.callback.__name__) if inspect.ismethod(s.callback) else s.callback
			s = message.subscribe(event = s.event, callback = c, id = id)
		return message

	def done(self):
		""" Deactivate the message, empty the next adjency list, and defuse all the active subscriptions """
		self.is_alive = False
		self.next = {}
		e_list = list(self.subscription.keys())
		for id in e_list:
			self.unsubscribe(id)

	def drop(self, id = 'dropped', event = None):
		""" Drop the simpype.Message object from the simulation.

		If event is not None, subscribe the message to the event and the default drop callback

		Args:
			id (str, optional):
				The id identifying in the log this drop action
			event (simpy.Event, optional):
				The event that will trigger the message dropping

		"""
		if event is None:
			self._drop(self, id)
		else:
			assert isinstance(event, simpy.Event)
			e = self.subscribe(event = event, callback = self._drop, id = id)

	def subscribe(self, event, callback, id):
		""" Subscribe the message to a given event which will execute a callback function.

		Args:
			event (simpy.Event):
				The simpy.Event to subscribe to
			callback (user-defined python function):
				The function to call upon event triggering
			id (str):
				The id identifying this subscription

		Returns:
			:class:`Subscription`

		"""
		assert isinstance(event, simpy.Event)
		assert callable(callback)
		if id in self.subscription:
			self.unsubscribe(id)
		s = Subscription(self.sim, self, event, callback, id)
		self.subscription[id] = s
		self.env.process(self._wait_event(s))
		return s

	def timestamp(self, description):
		""" Create and write a timestamp to the log file 
		
		Args:
			description (str):
				The timestamp description
		
		"""
		ts = Timestamp(self, self.env.now, self.resource, description)
		if self.log and self.location.log:
			self.sim.log.write(ts)
		return ts

	def unsubscribe(self, id):
		""" Unsubscribe the message from the subscription ``id``

		Args:
			id (any):
				The subscription id to unsubscribe

		"""
		assert id in self.subscription
		self.subscription[id].disable.succeed()
