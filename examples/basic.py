# Import SimPype module
import simpype
# Import python random module
import random

# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'simple')
# [Optional] Fix the seed for the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'mylog'
sim.log.file = False
sim.log.print = True

# [Mandatory] Add at least one generator to the simulation
gen0 = sim.add_generator(id = 'gen0')
# [Mandatory] Assign an arrival time
# Generator.random is a custom dictionary accepting the following format as values:
# generator.random[<some_id>] = {
# 	<initial_time> : lambda: <value>/<random_function>
#	...
# }
# Random values can be generated in the following way:
# 	generator.random[<some_id>].value
# The random value is:
# 	<value>/<random_function> the simulation time is equal or greater than (>=) <initial_time>, 0 otherwise
gen0.random['arrival'] = {
	# From t=0 to t=10, arrival is constant every 3s
	0	: lambda: 3.0,
	# From t=10 to t=20, arrival is uniform between 2.5 and 3.5
	10	: lambda: random.uniform(2.5, 3.5),
	# From t=20 to t=inf, arrival is expovariate with lambda 0.20
	20	: lambda: random.expovariate(0.20)
}

# [Mandatory] Add at least one resource to the simulation
res0 = sim.add_resource(id = 'res0')
# [Mandatory] Assign a service time
# Resource.random is a dictionary accepting the same Generator.random format
res0.random['service'] = {
	# From t=0 to t=10, service is constant at 1.5s
	0	: lambda: 1.5,
	# From t=10 to t=20, service is uniform between 1.5 and 2.5
	10	: lambda: random.uniform(1.5, 2.5),
	# From t=20 to t=inf, arrival is expovariate with lambda 2.0
	20	: lambda: random.expovariate(2.0)
}

# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(gen0, res0)

# [Mandatory] Run the simulation e.g. until t=30
#             sim.run calls Simpy's env.run
#             Any arg passed to sim.run is then passed to env.run
sim.run(until = 30)
