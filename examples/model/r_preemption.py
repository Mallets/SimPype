import simpype


class Resource(simpype.Resource):
	def __init__(self, sim, id, capacity = 1, pipe = None):
		super().__init__(sim, id, capacity, pipe)
		self.random['service'] = {0: lambda: 1}

	@simpype.resource.service	
	def service(self, message):
		if 'wait' not in message.property:
			message.property['wait'] = self.random['service'].value
		yield self.env.timeout(message.property['wait'].value)


# Do NOT remove
resource = lambda *args: Resource(*args)
