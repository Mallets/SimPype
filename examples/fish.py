import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'fish')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True
# [Optional] Log custom message properties
sim.log.property('species')
# [Mandatory] Add at least one generator to the simulation
fish = sim.add_generator(id = 'fish')
# [Mandatory] Assign an arrival time
fish.random['arrival'] = {
	0: lambda: random.expovariate(1.0 / 0.1)
}
fish.message.property['species'] = {
	0: lambda: random.choice(['cod', 'tuna', 'calamari'])
}


# [Mandatory] Add at least one resource to the simulation
dry = sim.add_resource(id = 'dry')
dry.random['service'] = {
	0: lambda: 60
}

# Add an additional resource
can = sim.add_resource(id = 'can')
can.random['service'] = {
	0: lambda: random.expovariate(1.0 / 20)
}

# Add an additional resource
grill = sim.add_resource(id = 'grill')
grill.random['service'] = {
	0: lambda: random.expovariate(1.0 / 60)
}

# Add an additional resource
selector = sim.add_resource(id = 'selector')
@simpype.resource.service(selector)
def selector_service(self, message):
	if message.property['species'].value == 'cod':
		message.next = dry
	elif message.property['species'].value == 'tuna':
		message.next = can
	elif message.property['species'].value == 'calamari':
		message.next = grill


# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(fish, selector)
p1 = sim.add_pipeline(selector, can)
p2 = sim.add_pipeline(selector, grill)
pM = sim.merge_pipeline(p0, p1, p2)

# [Mandatory] Run the simulation e.g. until t=2
sim.run(until = 2)
