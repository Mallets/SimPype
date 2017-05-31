import math

import simpype


class TokenBucket(simpype.Queue):
	def __init__(self, sim, pipe, id):
		super().__init__(sim, pipe, id)
		self.disable()
		self.capacity = float('inf')
		self.level = float('inf')
		self.rate = float('inf')
		self.last = self.env.now
		self.available = self.env.event()
		self.env.process(self._activate())

	@property
	def level(self):
		l = math.ceil(self._level + self.rate*(self.env.now - self.last))
		self._level = l if l < self.capacity else self.capacity
		self.last = self.env.now
		return self._level

	@level.setter
	def level(self, value):
		self._level = value

	def _activate(self):
		while True:
			yield self.available
			self.available = self.env.event()
			message = self.buffer[0]
			size = message.property['size'].value
			if self.level < size:
				yield self.env.timeout((1.0/self.rate)*(size-self.level))
			self.enable()
								
	@simpype.queue.push
	def push(self, message):
		if (len(self) + message.property['size'].value) <= self.capacity:
			self.buffer.append(message)
			if not self.available.triggered:
				self.available.succeed()
			return message
		else:
			message.drop('full')
			return None

	@simpype.queue.pop
	def pop(self):
		if len(self.buffer) > 0:
			message = self.buffer.pop(0)
			self.level = self.level - message.property['size'].value
			if len(self.buffer) == 0 or \
			self.level < self.buffer[0].property['size'].value:
				self.disable()
			return message
		else:
			return None

	def __len__(self):
		return sum([m.property['size'].value for m in self.buffer])


class Wfq(simpype.Pipe):
	def __init__(self, sim, resource, id):
		super().__init__(sim, resource, id)
		self.rate = pow(10,1)
		self.classes = 1

	@property
	def rate(self):
		return self._rate
	
	@rate.setter
	def rate(self, value):
		self._rate = value
		self._set_queue_param()

	@property
	def classes(self):
		return self._classes
	
	@classes.setter
	def classes(self, value):
		self._classes = value
		for i in range(len(self.queue), value):
			q = self.add_queue(id = i, model = 'p_wfq')
		self._set_queue_param()

	def _set_queue_param(self):
		fraction = sum([l for l in range(1, len(self.queue)+1)])
		for i in range(0, len(self.queue)):
			self.queue[i].rate = math.floor(self.rate*(i+1)/fraction)
			self.queue[i].capacity = math.floor(self.queue[i].rate)
			self.queue[i].level = math.floor(self.queue[i].rate)

	@simpype.pipe.dequeue
	def dequeue(self):
		queue = None
		size = float('inf')
		for q in [q for q in self.queue.values() if q.active.triggered]:
			s = q.buffer[0].property['size'].value
			if s <= q.level and s < size:
				queue = q
				size = s
		return queue.pop()

	@simpype.pipe.enqueue
	def enqueue(self, message):
		if 'priority' not in message.property:
			message.property['priority'] = 0
		if 'size' not in message.property:
			message.property['size'] = 1
		priority = message.property['priority'].value
		return self.queue[priority].push(message)


# Do NOT remove
queue = lambda *args: TokenBucket(*args)
pipe = lambda *args: Wfq(*args)
