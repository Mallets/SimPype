.. _example_basic:

=====
Basic
=====

The scenario of the simulation is the following:

.. code-block:: none

   |Generator| -> |Resource|

The scenario is so implemented with SimPype:

.. code-block:: python

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
    # 	<value>/<random_function> the simulation time is equal or greater
    #                             than (>=) <initial_time>, 0 otherwise
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

``sim.cfg`` stored under the ``mylog`` folder contains:

.. code-block:: none

    Simulation Seed: 42
    Simulation Time: 30.000000000
    Execution Time: 0.003305724

``sim.log`` stored under the ``mylog`` folder contains:

.. code-block:: none
    
    timestamp,message,seq_num,resource,event
    0.000000000,gen0,0,res0,pipe.in
    0.000000000,gen0,0,res0,pipe.out
    1.500000000,gen0,0,res0,resource.serve
    3.000000000,gen0,1,res0,pipe.in
    3.000000000,gen0,1,res0,pipe.out
    4.500000000,gen0,1,res0,resource.serve
    6.000000000,gen0,2,res0,pipe.in
    6.000000000,gen0,2,res0,pipe.out
    7.500000000,gen0,2,res0,resource.serve
    9.000000000,gen0,3,res0,pipe.in
    9.000000000,gen0,3,res0,pipe.out
    10.500000000,gen0,3,res0,resource.serve
    12.000000000,gen0,4,res0,pipe.in
    12.000000000,gen0,4,res0,pipe.out
    13.525010755,gen0,4,res0,resource.serve
    15.139426798,gen0,5,res0,pipe.in
    15.139426798,gen0,5,res0,pipe.out
    16.862637537,gen0,5,res0,resource.serve
    17.914456117,gen0,6,res0,pipe.in
    17.914456117,gen0,6,res0,pipe.out
    20.091155604,gen0,6,res0,resource.serve
    21.150927331,gen0,7,res0,pipe.in
    21.150927331,gen0,7,res0,pipe.out
    21.196403533,gen0,7,res0,resource.serve

