import simpype


class Cashier(simpype.Resource):
	def __init__(self, sim, id, capacity = 1, pipe = None):
		super().__init__(sim, id, capacity, pipe)
	
	@simpype.resource.service	
	def service(self, message):
		yield self.env.timeout(self.random['service'].value * message.property['size'].value)


# Do NOT remove
resource = lambda *args: Cashier(*args)
