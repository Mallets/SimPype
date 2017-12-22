.. _example_feature_lifetime:

========
Lifetime
========

The scenario of the simulation is the following:

.. code-block:: none

    |Generator| -> |Resource|

A `lifetime` is associated to the generated messages.
The message `expires` if the `lifetime` countdown occurs while waiting in the resource's pipe.
The scenario is so implemented with SimPype:

.. literalinclude:: ../../../examples/features/lifetime.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/lifetime/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/lifetime/run01/sim.log
