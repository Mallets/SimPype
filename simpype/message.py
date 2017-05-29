import copy
import inspect
import simpy

import simpype.message
import simpype.pipeline
import simpype.random
import simpype.resource
import simpype.simulation


class PropertyDict(dict):
	def __init__(self, sim):
		assert isinstance(sim, simpype.simulation.Simulation)
		super().__init__()
		self.sim = sim
		self.env = sim.env
	
	def __setitem__(self, key, value):
		if isinstance(value, Property):
			super().__setitem__(key, value)
		else:
			super().__setitem__(key, Property(self.sim, key, value))


class Property:
	def __init__(self, sim, name, value):
		assert isinstance(sim, simpype.simulation.Simulation)
		self.sim = sim
		self.env = sim.env
		self.name = name
		if isinstance(value, dict) and [f for f in value.values() if inspect.isfunction(f)]:
			self._random = simpype.random.Random(self.sim, value)
			self._value = self._random.value
		else:
			self._random = None
			self._value = value

	@property
	def value(self):
		return self._value

	def copy(self):
		property = Property(self.sim, self.name, self._value)
		property._random = self._random
		return property

	def refresh(self):
		if isinstance(self._random, simpype.random.Random):
			self._value = self._random.value


class Timestamp:
	def __init__(self, message, timestamp, resource, event):
		assert isinstance(message, Message)
		assert isinstance(resource,simpype.resource.Resource)
		self.message = message
		self.timestamp = float(timestamp)
		self.resource = resource
		self.event = str(event)


class Subscription:
	def __init__(self, sim, message, event, callback):
		assert isinstance(sim, simpype.simulation.Simulation)
		assert isinstance(message, Message)
		assert callable(callback)
		self.sim = sim
		self.env = sim.env
		self.message = message
		self.event = event
		self.callback = callback
		self.disable = self.env.event()


class Message:
	def __init__(self, sim, resource, id):
		assert isinstance(sim, simpype.simulation.Simulation)
		assert isinstance(resource, simpype.resource.Resource)
		self.sim = sim					
		self.env = sim.env
		self.id = id
		self.generated = self.env.now
		self.generator = resource
		self.is_alive = True
		self.next = {}
		self.visited = []
		self.resource = resource
		self.pipeline = simpype.pipeline.Pipeline(self.sim, self.id)
		self.property = PropertyDict(self.sim)
		self.queue = None
		self.seq_num = 0
		self.subscription = {}
		# Init
		self.property['size'] = 1
		self.property['priority'] = 0

	def __setattr__(self, name, value):
		if name == 'next':
			if isinstance(value, simpype.resource.Resource):
				value = {value.pipe.resource.id: value.pipe}
			elif isinstance(value, simpype.pipeline.Pipeline):
				value = {value.first.resource.id: value.first}
		elif name == 'pipeline':
			assert isinstance(value, simpype.pipeline.Pipeline)
		elif name == 'queue':
			assert isinstance(value, (simpype.queue.Queue, type(None)))
		elif name == 'resource':
			assert isinstance(value, simpype.resource.Resource)
		self.__dict__[name] = value
		if name == 'pipeline':
			if hasattr(self, 'resource'):
				self._update_next()
		elif name == 'resource':
			self.visited.append(self.resource)
			if hasattr(self, 'pipeline'):
				self._update_next()

	def _drop(self, message, cause):
		self.done()
		if self.queue is None:
			self.resource._message_dropped(self, cause)
		else:
			self.queue._message_dropped(self, cause)

	def _update_next(self):
		if self.resource.id in self.pipeline.resource:
			self.next = {p.id: p for p in self.pipeline.resource[self.resource.id]}
		else:
			self.next = {}

	def _wait_event(self, subscription):
		active = True
		while active:
			e = subscription.event
			value = yield e | subscription.disable
			if e in value and self.is_alive:
				subscription.callback(self, value[e])
			else:
				active = False
			if isinstance(e, simpy.events.Timeout):
				active = False
	
	def copy(self):
		message = Message(self.sim, self.generator, self.id)
		message.generated = copy.deepcopy(self.generated)
		message.resource = self.resource
		message.queue = self.queue
		message.seq_num = copy.deepcopy(self.seq_num)
		message.visited = copy.copy(self.visited)
		message.is_alive = copy.deepcopy(self.is_alive)
		message.next = copy.copy(self.next)
		message.pipeline = copy.copy(self.pipeline)
		for p in self.property.values():
			message.property[p.name] = p.copy()
		for id,s in self.subscription.items():
			c = getattr(message, s.callback.__name__) if inspect.ismethod(s.callback) else s.callback
			s = message.subscribe(event = s.event, callback = c, id = id)
		return message

	def done(self):
		self.is_alive = False
		self.next = {}
		e_list = list(self.subscription.keys())
		for id in e_list:
			self.unsubscribe(id)

	def drop(self, id = 'dropped', event = None):
		if event is None:
			self._drop(self, id)
		else:
			e = self.subscribe(event = event, callback = self._drop, id = id)

	def subscribe(self, callback, event, id = None):
		assert callable(callback)
		if event in self.subscription:
			self.unsubscribe(event)
		s = Subscription(self.sim, self, event, callback)
		self.env.process(self._wait_event(s))
		if id is None:
			self.subscription[s] = s
		else:
			self.subscription[id] = s
		return s

	def timestamp(self, event):
		ts = Timestamp(self, self.env.now, self.resource, event)
		self.sim.log.write(ts)
		return ts

	def unsubscribe(self, subscription):
		assert subscription in self.subscription
		self.subscription[subscription].disable.succeed()
		del self.subscription[subscription]
