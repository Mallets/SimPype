.. _example_splitter:

========
Splitter
========

The scenario of the simulation is the following:

.. code-block :: none

                               /-> |Resource #0|
   |Generator| -> |Splitter| -(
                               \-> |Resource #1|

Where messages with even sequence number are sent to `Resource #0` and
messages with odd  sequence number are sent to `Resource #1` instead.
The scenario is so implemented with SimPype:

.. code-block :: python

	import simpype
	import random

	# [Mandatory] Create a SimPype simulation object
  	sim = simpype.Simulation(id = 'splitter')
	# [Optional] Fix the seed used by the pseudo-random generator
	sim.seed = 42

	# Create a generator
	gen0 = sim.add_generator(id = 'gen')
	# Assign an arrival time
	gen0.random['arrival'] = {
		0: lambda: 3.0,
	}

	# Add a resource
	res0 = sim.add_resource(id = 'res0')
	res0.random['service'] = {
		0 : lambda: 2.0,
	}

	# Add a resource
	res1 = sim.add_resource(id = 'res1')
	res1.random['service'] = {
		0 : lambda: 8.0,
	}

	# Add a splitter
	splitter = sim.add_resource(id = 'splitter')
	@simpype.resource.service(splitter)
	def service(self, message):
        yield self.env.timeout(1.0)
		if message.seq_num % 2 == 0:
			message.next = res0
		else:
			message.next = res1

	# Add a pipeline connecting the generator to the resource
	p0 = sim.add_pipeline(gen0, splitter)
	p1 = sim.add_pipeline(splitter, res0)
	p2 = sim.add_pipeline(splitter, res1)
	pM = sim.merge_pipeline(p0, p1, p2)

	# Run until t=30
	sim.run(until = 30)


``sim.cfg`` stored under the ``log`` folder contains:

.. code-block :: none

    Simulation Seed: 42
    Simulation Time: 30.000000000
    Execution Time: 0.006984534

``sim.log`` stored under the ``log`` folder contains:

.. code-block :: none

    timestamp,message,seq_num,resource,event
    0.000000000,gen,0,splitter,pipe.default.in
    0.000000000,gen,0,splitter,pipe.default.out
    1.000000000,gen,0,splitter,resource.serve
    1.000000000,gen,0,res0,pipe.default.in
    1.000000000,gen,0,res0,pipe.default.out
    3.000000000,gen,1,splitter,pipe.default.in
    3.000000000,gen,0,res0,resource.serve
    3.000000000,gen,1,splitter,pipe.default.out
    4.000000000,gen,1,splitter,resource.serve
    4.000000000,gen,1,res1,pipe.default.in
    4.000000000,gen,1,res1,pipe.default.out
    6.000000000,gen,2,splitter,pipe.default.in
    6.000000000,gen,2,splitter,pipe.default.out
    7.000000000,gen,2,splitter,resource.serve
    7.000000000,gen,2,res0,pipe.default.in
    7.000000000,gen,2,res0,pipe.default.out
    9.000000000,gen,3,splitter,pipe.default.in
    9.000000000,gen,2,res0,resource.serve
    9.000000000,gen,3,splitter,pipe.default.out
    10.000000000,gen,3,splitter,resource.serve
    10.000000000,gen,3,res1,pipe.default.in
    12.000000000,gen,4,splitter,pipe.default.in
    12.000000000,gen,1,res1,resource.serve
    12.000000000,gen,4,splitter,pipe.default.out
    12.000000000,gen,3,res1,pipe.default.out
    13.000000000,gen,4,splitter,resource.serve
    13.000000000,gen,4,res0,pipe.default.in
    13.000000000,gen,4,res0,pipe.default.out
    15.000000000,gen,5,splitter,pipe.default.in
    15.000000000,gen,4,res0,resource.serve
    15.000000000,gen,5,splitter,pipe.default.out
    16.000000000,gen,5,splitter,resource.serve
    16.000000000,gen,5,res1,pipe.default.in
    18.000000000,gen,6,splitter,pipe.default.in
    18.000000000,gen,6,splitter,pipe.default.out
    19.000000000,gen,6,splitter,resource.serve
    19.000000000,gen,6,res0,pipe.default.in
    19.000000000,gen,6,res0,pipe.default.out
    20.000000000,gen,3,res1,resource.serve
    20.000000000,gen,5,res1,pipe.default.out
    21.000000000,gen,7,splitter,pipe.default.in
    21.000000000,gen,6,res0,resource.serve
    21.000000000,gen,7,splitter,pipe.default.out
    22.000000000,gen,7,splitter,resource.serve
    22.000000000,gen,7,res1,pipe.default.in
    24.000000000,gen,8,splitter,pipe.default.in
    24.000000000,gen,8,splitter,pipe.default.out
    25.000000000,gen,8,splitter,resource.serve
    25.000000000,gen,8,res0,pipe.default.in
    25.000000000,gen,8,res0,pipe.default.out
    27.000000000,gen,9,splitter,pipe.default.in
    27.000000000,gen,8,res0,resource.serve
    27.000000000,gen,9,splitter,pipe.default.out
    28.000000000,gen,5,res1,resource.serve
    28.000000000,gen,9,splitter,resource.serve
    28.000000000,gen,9,res1,pipe.default.in
    28.000000000,gen,7,res1,pipe.default.out
