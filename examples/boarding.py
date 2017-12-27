import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'boarding')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True
# [Optional] Configure the path containting the models for the simulation. 
# [Default] Current working directory
sim.model.dir = 'examples/model'

# Create a generator
first = sim.add_generator(id = 'first')
first.to_send = 12
# Assign an arrival time
first.random['arrival'] = {
	0   : lambda: random.expovariate(1.0 / 900),
	1800: lambda: random.expovariate(1.0 / 30)
}
# Create a generator
business = sim.add_generator(id = 'business')
business.to_send = 24
# Assign an arrival time
business.random['arrival'] = {
	0   : lambda: random.expovariate(1.0 / 450),
	900 : lambda: random.expovariate(1.0 / 60),
	1800: lambda: random.expovariate(1.0 / 30),
}
# Create a generator
economy = sim.add_generator(id = 'economy')
economy.to_send = 160
# Assign an arrival time
economy.random['arrival'] = {
	0   : lambda: random.expovariate(1.0 / 60),
	600 : lambda: random.expovariate(1.0 / 30),
	1200: lambda: random.expovariate(1.0 / 10),
}

# Add a resource
gate = sim.add_resource(id = 'gate', pipe = 'p_priority')
gate.random['service'] = {
	# The gate opens 30 mins from the simulation start
	# Check boarding pass and passport takes ~10s
	1800: lambda: random.expovariate(1.0 / 10)
}

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(first, gate)
p1 = sim.add_pipeline(business, gate)
p2 = sim.add_pipeline(economy, gate)

# Run the simulation
sim.run()
