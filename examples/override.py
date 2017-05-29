import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'override')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42

# Create a generator
gen0 = sim.add_generator(id = 'gen')
# Assign an arrival time
gen0.random['arrival'] = {
	0: lambda: 3.0,
}
# Assign a size to the message
gen0.message.property['size'] = {
	0: lambda: random.randint(1,3),
}
# Add the size of the message to the log
sim.log.property('size')

# Add a resource
res0 = sim.add_resource(id = 'res')
res0.random['service'] = {
	0 : lambda: 2.0,
}

@simpype.resource.service(res0)
def service(self, message):
	yield self.env.timeout(self.random['service'].value * message.property['size'].value)

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(gen0, res0)

# Run until t=30
sim.run(until = 30)
