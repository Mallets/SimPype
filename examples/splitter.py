import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'splitter')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42

# Create a generator
gen0 = sim.add_generator(id = 'gen')
# Assign an arrival time
gen0.random['arrival'] = {
	0: lambda: 3.0,
}

# Add a resource
res0 = sim.add_resource(id = 'res0')
res0.random['service'] = {
	0 : lambda: 2.0,
}

# Add a resource
res1 = sim.add_resource(id = 'res1')
res1.random['service'] = {
	0 : lambda: 8.0,
}

# Add a splitter
splitter = sim.add_resource(id = 'splitter')
@simpype.resource.service(splitter)
def service(self, message):
	if message.seq_num % 2 == 0:
		message.next = res0
	else:
		message.next = res1

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(gen0, splitter)
p1 = sim.add_pipeline(splitter, res0)
p2 = sim.add_pipeline(splitter, res1)
pM = sim.merge_pipeline(p0, p1, p2)

# Run until t=30
sim.run(until = 30)
