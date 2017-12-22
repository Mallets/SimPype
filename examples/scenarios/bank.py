# Import SimPype module
import simpype
# Import python random module
import random

NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience
TIME_IN_BANK = 12.0 # Time spent in the bank by the customers

# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'bank')
# [Optional] Fix the seed for the pseudo-random generator
sim.seed = 42
# [Optional] Configure the log directory. 
# [Default] Log are store by default in the 'current working directory/log'
sim.log.dir = 'log'
# [Optional] Disable the logging to file and print to console instead
#sim.log.file = False
#sim.log.print = True

# [Mandatory] Add at least one generator to the simulation
customer = sim.add_generator(id = 'customer')
# Generate 5 customer arrivals
customer.to_send = NEW_CUSTOMERS
# [Mandatory] Assign an arrival time
customer.random['arrival'] = {
	0: lambda: random.expovariate(1.0 / INTERVAL_CUSTOMERS)
}
# Assign a patience to the customer
customer.message.property['lifetime'] = {
	0: lambda: random.uniform(MIN_PATIENCE, MAX_PATIENCE)
}

# [Mandatory] Add at least one resource to the simulation
counter = sim.add_resource(id = 'counter')
# [Mandatory] Assign a service time
counter.random['service'] = {
	0: lambda: random.expovariate(1.0 / TIME_IN_BANK)
}

# Define the resource service behavior when receiving a message
@simpype.resource.service(counter)
def service(self, message):
	# Unsubscribe the customer from the lifetime event so to not leave
	# while being served.
	message.unsubscribe('lifetime')
	# Wait a random time according to random.expovariate(0.10) distribution
	yield self.env.timeout(self.random['service'].value)

# [Mandatory] Add a pipeline connecting the generator and the resource
p0 = sim.add_pipeline(customer, counter)

# [Mandatory] Run the simulation
# The simulations stops if no events are available 
# (e.g., 5 customers have been served)
sim.run()
