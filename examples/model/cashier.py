import random
import simpype


class Cashier(simpype.Resource):
	def __init__(self, sim, id, capacity = 1, pipe = None):
		super().__init__(sim, id, capacity, pipe)
		self.random['scan'] = {0: lambda: 2.0}
		self.random['payment'] = {0: lambda: random.uniform(20, 60)}
	
	@simpype.resource.service	
	def service(self, message):
		yield self.env.timeout(self.random['scan'].value * message.property['items'].value)
		yield self.env.timeout(self.random['payment'].value)


# Do NOT remove
resource = lambda *args: Cashier(*args)
