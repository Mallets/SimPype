import simpype


class ResourcePreemption(simpype.Resource):
	def __init__(self, sim, id, capacity = 1, pipe = None):
		super().__init__(sim, id, capacity, pipe)
		# This is overwritten later in the simulaiton file
		self.random['service'] = {
			0: lambda: 1.0
		}

	@simpype.resource.service	
	def service(self, message):
		if 'wait' not in message.property:
			message.property['wait'] = message.property['items'].value * self.random['service'].value
		yield self.env.timeout(message.property['wait'].value)


# Do NOT remove
resource = lambda *args: ResourcePreemption(*args)
