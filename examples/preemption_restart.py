import simpype
import random


# [Mandatory] Create a SimPype simulation object
sim = simpype.Simulation(id = 'preemption_restart')
# [Optional] Fix the seed used by the pseudo-random generator
sim.seed = 42
# [Optional] Configure the path containting the models for the simulation. 
# [Default] Current working directory
sim.model.dir = 'examples/model'

# Create a generator
gen0 = sim.add_generator(id = 'gen0')
# Assign an arrival time
gen0.random['arrival'] = {0: lambda: random.expovariate(1.0/60)}
gen0.message.property['priority'] = 0
# Create a generator
gen1 = sim.add_generator(id = 'gen1')
# Assign an arrival time
gen1.random['arrival'] = {0: lambda: random.expovariate(1.0/60)}
gen1.message.property['priority'] = 1

# Add a resource
res0 = sim.add_resource(id = 'res0', pipe = 'p_preemption')
res0.random['service'] = {0: lambda: random.expovariate(1.0/90)}

# Add a pipiline connecting the generator to the resource
p0 = sim.add_pipeline(gen0, res0)
p1 = sim.add_pipeline(gen1, res0)

# Run until t=300
sim.run(until = 300)
