.. _logging:

==========
Log system
==========

SimPype automatically logs the simulation results in a log directory having the following 
structure in case of our simple simulation (see :ref:`simulation`):

.. code-block:: none

    <working directory>
    |-- simple.py 
    |-- log
        |-- simple
            |-- <simulation date i.e. '2017-06-05 10:31:30.512772'>
                |-- sim.cfg
                `-- sim.log


``sim.cfg`` contains information about the simulation environment and has the following format:

.. code-block:: none

    Simulation Seed: 1369068917606710528
    Simulation Time: 5.000000000
    Execution Time: 0.003524998

``sim.log`` contains the log of the simulation events and looks like:

.. code-block:: none

    timestamp,message,seq_num,resource,event
    0.000000000,gen0,0,res0,pipe.default.in
    0.000000000,gen0,0,res0,pipe.default.out
    0.252555552,gen0,0,res0,resource.serve
    0.722431377,gen0,1,res0,pipe.default.in
    0.722431377,gen0,1,res0,pipe.default.out
    0.869881996,gen0,1,res0,resource.serve
    1.413266674,gen0,2,res0,pipe.default.in
    1.413266674,gen0,2,res0,pipe.default.out
    1.478382544,gen0,2,res0,resource.serve
    2.833221707,gen0,3,res0,pipe.default.in
    2.833221707,gen0,3,res0,pipe.default.out
    3.117096444,gen0,3,res0,resource.serve
    3.455033536,gen0,4,res0,pipe.default.in
    3.455033536,gen0,4,res0,pipe.default.out
    4.174690658,gen0,5,res0,pipe.default.in
    4.301555284,gen0,6,res0,pipe.default.in
    4.587560103,gen0,4,res0,resource.serve
    4.587560103,gen0,5,res0,pipe.default.out
    4.898210753,gen0,5,res0,resource.serve
    4.898210753,gen0,6,res0,pipe.default.out
    4.975600594,gen0,6,res0,resource.serve

Let's analyze the first three log entries:

.. code-block:: none

    timestamp,message,seq_num,resource,event
    0.000000000,gen0,0,res0,pipe.default.in

1. A message with id ``gen0`` and sequence number ``0`` has been enqueued to the pipe of resource ``res0`` in the queue ``default`` at simulation time ``0.000000000``.

.. code-block:: none

    timestamp,message,seq_num,resource,event
    0.000000000,gen0,0,res0,pipe.default.out

2. The message with id ``gen0`` and sequence number ``0`` has been dequeued from the pipe of resource ``res0`` and queue ``default`` at simulation time ``0.000000000``. This means that the resource was available as soon as the message reached the resource. Therefore, the time spent waiting in the pipe was ``0``.

.. code-block:: none

    timestamp,message,seq_num,resource,event
    0.252555552,gen0,0,res0,resource.serve

3. The resource ``res0`` served the message with id ``gen0`` and sequence number ``0`` at simulation time ``0.252555552``.

Change log directory
====================

You can change the default log directory by setting the following variable in the simulation environment:

.. code-block:: python

    import simpype

    sim = simpype.Simulation(id = 'simple')
    sim.log.dir = '<your preferred dir>'

Please make sure you have writing permissions to ``<your preferred dir>``.

Log custom message properties
=============================

You can configure SimPype's logger to log any additional message properties as you wish by calling the following function in the simulation environment:

.. code-block:: python

    import simpype

    sim = simpype.Simulation(id = 'simple')
    sim.log.property('test')

    gen0.message.property['test'] = {
        0: lambda: 1
    }

``sim.log`` file now will containt a column containing the value of ``test`` message property:

.. code-block:: none

    timestamp,message,seq_num,resource,event,test
    0.000000000,gen0,0,res0,pipe.default.in,1

If a message does not have the custom property, SimPype logs ``NA`` instead.

Print the logs
==============

If you prefer to print the logs instead of storing them in a file, you can do it by setting the following variables in the simulation environment:

.. code-block:: python

    import simpype

    sim = simpype.Simulation(id = 'simple')
    sim.log.file = False
    sim.log.print = True
