import simpype


class Generator(simpype.Resource):
	def __init__(self, sim, id):
		super().__init__(sim, id)
		self.message = simpype.Message(self.sim, self, self.id)
		self.counter = 0
		self.to_send = float("inf")
		# Init
		self.message.is_alive = False
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
		more = True
		while self.counter < self.to_send and more:
			val = self.random['arrival'].value
			if val is None:
				more = False
			else:
				yield self.env.timeout(val)
				message = self.gen_message()
				self.send(message)
				self.counter = self.counter + 1

# Do NOT remove
resource = lambda *args: Generator(*args)
