import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'supermarket')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the path containting the models for the simulation. 
# [Default] Current working directory
sim.model.dir = 'model'

# Create a generator
gen0 = sim.add_generator(id = 'gen')
# Assign an arrival time
gen0.random['arrival'] = {0: lambda: random.expovariate(1.0/60)}

# Assign a size to the message
gen0.message.property['items'] = {0: lambda: random.randint(1,10)}
# Add the size of the message to the log
sim.log.property('items')

# Add a resource
cashier = sim.add_resource(id = 'cashier', model = 'cashier')

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(gen0, cashier)

# Run until t=300
sim.run(until = 300)
