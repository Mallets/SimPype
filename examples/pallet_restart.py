import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'pallet_restart')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True
# [Optional] Log custom message properties
sim.log.property('items')
# [Optional] Configure the path containting the models for the simulation. 
# [Default] Current working directory
sim.model.dir = 'examples/model'

# Create a generator
urgent = sim.add_generator(id = 'urgent')
# Assign an arrival time
urgent.random['arrival'] = {
	0: lambda: random.expovariate(1.0 / 3600)
}
urgent.message.property['priority'] = 'urgent'
urgent.message.property['items'] = {
	0: lambda: random.randint(1, 5)
}
# Create a generator
normal = sim.add_generator(id = 'normal')
# Assign an arrival time
normal.random['arrival'] = {
	0: lambda: random.expovariate(1.0 / 300)
}
normal.message.property['priority'] = 'normal'
normal.message.property['items'] = {
	0: lambda: random.randint(10, 30)
}

# Add a resource
worker = sim.add_resource(id = 'worker', pipe = 'p_preemption')
worker.random['service'] = {
	0: lambda: random.expovariate(1.0 / 10)
}
# Service time depends on the number of items
@simpype.resource.service(worker)
def service(self, message):
	yield self.env.timeout(message.property['items'].value * self.random['service'].value)

# Add a pipeline connecting the generator to the resource
p0 = sim.add_pipeline(urgent, worker)
p1 = sim.add_pipeline(normal, worker)

# Run until t=28800 (8 hours)
sim.run(until = 28800)
