import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'splitter')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True

# [Mandatory] Add at least one generator to the simulation
gen0 = sim.add_generator(id = 'gen0')
# [Mandatory] Assign an arrival time
gen0.random['arrival'] = {0: lambda: 3.0}

# [Mandatory] Add at least one resource to the simulation
res0 = sim.add_resource(id = 'res0')
# [Mandatory] Assign a service time
res0.random['service'] = {0 : lambda: 2.0}

# Add an additional resource
res1 = sim.add_resource(id = 'res1')
res1.random['service'] = {0 : lambda: 8.0}

# Add an additional resource acting as splitter
splitter = sim.add_resource(id = 'splitter')
# Define the splitter service behavior when receiving a message
@simpype.resource.service(splitter)
def service(self, message):
	yield self.env.timeout(1.0)
	if message.seq_num % 2 == 0:
		message.next = res0
	else:
		message.next = res1

# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(gen0, splitter)
p1 = sim.add_pipeline(splitter, res0)
p2 = sim.add_pipeline(splitter, res1)
pM = sim.merge_pipeline(p0, p1, p2)

# [Mandatory] Run the simulation e.g. until t=30
sim.run(until = 30)
