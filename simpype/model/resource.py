import simpype.resource


class Resource(simpype.resource.Resource):
	def __init__(self, sim, id, capacity = 1, pipe = None):
		super().__init__(sim, id, capacity)
		self.random['service'] = {0: lambda: 0}
	
	@simpype.resource.service
	def service(self, message):
		yield self.env.timeout(self.random['service'].value)


# Do NOT remove
resource = lambda *args: Resource(*args)
