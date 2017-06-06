.. _example_renege:

======
Renege
======

The scenario of the simulation is the following:

.. code-block:: none

    |Generator| -> |Resource|

A `lifetime` is associated to the generated messages.
The message `expires` if the `lifetime` countdown occurs while waiting in the resource's pipe.
The scenario is so implemented with SimPype:

.. code-block:: python
    
    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    sim.seed = 42

    gen0 = sim.add_generator(id = 'gen0')
    gen0.random['arrival'] = {0: lambda: random.expovariate(0.20)}
    # Assign a lifetime to the messages
    gen0.message.property['lifetime'] = 1.75

    res0 = sim.add_resource(id = 'res0')
    res0.random['service'] = {0: lambda: random.expovariate(0.10)}

    @simpype.resource.service(res0)
    def service(self, message):
        # Unsubscribe from 'lifetime'. Otherwise the message could 'expire'
        # while is being served.
        message.unsubscribe('lifetime')
        yield self.env.timeout(self.random['service'].value)

    p0 = sim.add_pipeline(gen0, res0)

    sim.run(until = 30)

``sim.cfg`` stored under the ``log`` folder contains:

.. code-block:: none

    Simulation Seed: 42
    Simulation Time: 30.000000000
    Execution Time: 0.004337532

``sim.log`` stored under the ``log`` folder contains:

.. code-block:: none
     
    timestamp,message,seq_num,resource,event
    0.000000000,gen0,0,res0,pipe.default.in
    0.000000000,gen0,0,res0,pipe.default.out
    0.253288390,gen0,0,res0,resource.serve
    5.100301436,gen0,1,res0,pipe.default.in
    5.100301436,gen0,1,res0,pipe.default.out
    6.708421757,gen0,2,res0,pipe.default.in
    7.626163293,gen0,1,res0,resource.serve
    7.626163293,gen0,2,res0,pipe.default.out
    13.376385121,gen0,3,res0,pipe.default.in
    15.126385121,gen0,3,res0,pipe.default.expired
    18.917893381,gen0,2,res0,resource.serve
    24.512825619,gen0,4,res0,pipe.default.in
    24.512825619,gen0,4,res0,pipe.default.out
    24.967587642,gen0,5,res0,pipe.default.in
    25.118838528,gen0,6,res0,pipe.default.in
    26.352422007,gen0,7,res0,pipe.default.in
    26.717587642,gen0,5,res0,pipe.default.expired
    26.868838528,gen0,6,res0,pipe.default.expired
    28.102422007,gen0,7,res0,pipe.default.expired
    29.871999647,gen0,8,res0,pipe.default.in
    29.993287213,gen0,4,res0,resource.serve
    29.993287213,gen0,8,res0,pipe.default.out
