# Import SimPype module
import simpype
# Import python random module
import random

# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'simple')
# [Optional] Fix the seed for the pseudo-random generator
sim.seed = 42

# [Mandatory] Add at least one generator to the simulation
gen0 = sim.add_generator(id = 'gen0')
# [Mandatory] Assign an arrival time
gen0.random['arrival'] = {0: lambda: random.expovariate(0.20)}
# Assign a lifetime to the messages
gen0.message.property['lifetime'] = 1.75

# [Mandatory] Add at least one resource to the simulation
res0 = sim.add_resource(id = 'res0')
# [Mandatory] Assign a service time
res0.random['service'] = {0: lambda: random.expovariate(0.10)}

@simpype.resource.service(res0)
def service(self, message):
	message.unsubscribe('lifetime')
	yield self.env.timeout(self.random['service'].value)

# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(gen0, res0)

# [Mandatory] Run the simulation e.g. until t=30
sim.run(until = 30)
