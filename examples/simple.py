import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'simple')
# [Optional] Fix the seed for the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Current working directory/log
sim.log.dir = 'mylog'
# [Optional] Configure the path containting the models for the simulation. 
# [Default] Current working directory
sim.model.dir = 'mymodel'

# Create a generator
gen0 = sim.add_generator(id = 'gen')
# Assign an initial time
gen0.random['initial'] = {
	# Start at time = 1
	0	: lambda: 1.0
}
# Assign an arrival time
gen0.random['arrival'] = {
	# From t=0 to t=10, arrival is constant every 2t
	0	: lambda: 3.0,
	# From t=10 to t=20, arrival is uniform
	10	: lambda: random.uniform(2.5, 3.5),
	# From t=20 to t=inf, arrival is expovariate
	20	: lambda: random.expovariate(0.20)
}

# Add a resource
res0 = sim.add_resource(id = 'res')
res0.random['service'] = {
	# From t=0 to t=10, service is constant at 1.5t
	0	: lambda: 1.5,
	# From t=10 to t=20, service is uniform
	10	: lambda: random.uniform(1.5, 2.5),
	# From t=20 to t=inf, arrival is expovariate
	20	: lambda: random.expovariate(2.0)
}

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(gen0, res0)

# Run until t=30
sim.run(until = 30)
