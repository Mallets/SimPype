.. _example_pallet_norestart:

==========================================
Pallet preparation - Preemption no restart
==========================================

SimPype features used in this example: `Random variables <../tutorial/random.html>`_, `Resource custom model <../tutorial/resource.html#custom-model>`_, `Pipe custom model <../tutorial/pipe.html#custom-model>`_, `Log custom message properties <../tutorial/logging.html#log-custom-message-properties>`_.

The scenario of the simulation is the following:

.. code-block:: none

   |Urgent order| -\
                    ) -> |Worker|
   |Normal order| -/

This example models a working day (8 hours) of a  ``worker`` in a warehouse.
The worker's job is to prepare a pallet upon receiving an order.
There are two types of orders:

- Urgent
- Normal

Each order comprises a number of items to be packed on the same pallet.
Urgent orders ``preempt`` normal orders. 
This means that if an urgent order is received while the worker is preparing the pallet for a normal order, the worker will stop what is doing and will immedietaly start preparing the pallet for the urgent order.
Once the urgent pallet is prepare, the worker will resume the preparation of the pallet of the normal order.

This kind of interaction is usually called **preemption with no restart**.  

The scenario is so implemented with SimPype:

.. literalinclude:: ../../examples/pallet_norestart.py
   :language: python

Where pipe model ``p_preemption`` is so implemented:

.. literalinclude:: ../../examples/model/p_preemption.py

And resource model ``r_preemption`` is so implemented:

.. literalinclude:: ../../examples/model/r_preemption.py


``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/pallet_norestart/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/pallet_norestart/run01/sim.log
