# Import SimPype module
import simpype
# Import python random module
import random

# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'supermarket')
# [Optional] Fix the seed for the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True

# [Mandatory] Add at least one generator to the simulation
mom = sim.add_generator(id = 'mom')
# [Mandatory] Assign an arrival time
mom.random['arrival'] = {
	# 0h
	0: lambda: random.expovariate(1.0 / 60.0),
	# 1h
	3600: lambda: random.expovariate(1.0 / 300.0),
	# 2h
	7200: lambda: random.expovariate(1.0 / 180.0),
	# 3h
	10800: lambda: random.expovariate(1.0 / 600.0),
}
mom.message.property['items'] = {
	# 0h
	0: lambda: random.randint(10, 50),
	# 1h
	3600: lambda: random.randint(5, 25),
	# 2h
	7200: lambda: random.randint(15, 45),
	# 3h
	10800: lambda: random.randint(5, 50),
}

# [Mandatory] Add at least one generator to the simulation
single = sim.add_generator(id = 'single')
# [Mandatory] Assign an arrival time
single.random['arrival'] = {
	# 0h
	0: lambda: random.expovariate(1.0 / 3600.0),
	# 1h
	3600: lambda: random.expovariate(1.0 / 3600.0),
	# 2h
	7200: lambda: random.expovariate(1.0 / 1800.0),
	# 3h
	10800: lambda: random.expovariate(1.0 / 30.0),
}
single.message.property['items'] = {
	# 0h
	0: lambda: random.randint(10, 50),
	# 1h
	3600: lambda: random.randint(5, 25),
	# 2h
	7200: lambda: random.randint(3, 15),
	# 3h
	10800: lambda: random.randint(1, 5),
}

# [Mandatory] Add at least one resource to the simulation
cashier = sim.add_resource(id = 'cashier')
# Define the cashier service behavior when receiving a message
@simpype.resource.service(cashier)
def service(self, message):
	for i in range(0, message.property['items'].value):
		yield self.env.timeout(random.expovariate(1.0 / 2.0))
	yield self.env.timeout(random.expovariate(1.0 / 30.0))

# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(mom, cashier)
p1 = sim.add_pipeline(single, cashier)

# [Mandatory] Run the simulation for 4h (14400s = 60 x 60 x 4)
sim.run(until = 14400)
