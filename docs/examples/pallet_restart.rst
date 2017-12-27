.. _example_pallet_restart:

============================================
Pallet preparation - Preemption with restart
============================================

SimPype features used in this example: `Random variables <../tutorial/random.html>`_, `Resource inline customization <../tutorial/resource.html#inline-customization>`_, `Pipe custom model <../tutorial/pipe.html#custom-model>`_, `Log custom message properties <../tutorial/logging.html#log-custom-message-properties>`_.

The scenario of the simulation is the following:

.. code-block:: none

   |Urgent order| -\
                    ) -> |Worker|
   |Normal order| -/

The scenario description is the same as the one in `Pallet preparation - Preemption no restart <pallet_norestart.html>`_.
The difference resides in the fact that the worker will restart the pallet preparation from scratch if preempted.
This means that the worker will not resume the pallet preparation but rather will start again the preparation from the beginning. 
The worker pipe model is the same while the resource model is sligthly different (it does not consider the ``wait`` message property).
The difference in the code is highlighted below.

This kind of interaction is usually called **preemption with restart**.  

The scenario is so implemented with SimPype:

.. literalinclude:: ../../examples/pallet_restart.py
   :language: python
   :emphasize-lines: 43-50

Where pipe model ``p_preemption`` is so implemented:

.. literalinclude:: ../../examples/model/p_preemption.py

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/pallet_restart/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/pallet_restart/run01/sim.log
