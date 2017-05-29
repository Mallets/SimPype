import copy
import random

import simpype.message
import simpype.resource


class Generator(simpype.resource.Resource):
	def __init__(self, sim, id):
		super().__init__(sim, id)
		self.message = simpype.message.Message(self.sim, self, self.id)
		self.counter = 0
		self.to_send = float("inf")
		# Init
		self.message.is_alive = False
		self.random['initial'] = {0: lambda: 0}
		self.random['arrival'] = {0: lambda: float("inf")}
		self.a_gen = self.env.process(self.h_gen())

	def gen_message(self):
		message = self.message.copy()
		message.seq_num = self.counter
		message.generated = self.env.now
		for p in message.property.values():
			p.refresh()
		if 'lifetime' in message.property:
			message.drop('lifetime', self.env.timeout(message.property['lifetime'].value, 'expired'))
		message.is_alive = True
		return message

	def h_gen(self):
		while self.counter < self.to_send:
			if self.counter == 0:
				yield self.env.timeout(self.random['initial'].value)
			message = self.gen_message()
			self.send(message)
			yield self.env.timeout(self.random['arrival'].value)
			self.counter = self.counter + 1

# Do NOT remove
resource = lambda *args: Generator(*args)
