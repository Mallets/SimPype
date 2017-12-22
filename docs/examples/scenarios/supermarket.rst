.. _example_scenario_supermarket:

===========
Supermarket
===========

The scenario of the simulation is the classical bank renege:

.. code-block:: none

      |Mom| -\
              ) -> |Cashier|
   |Single| -/

This example models a supermarket with two type of customers arriving at different times and purchasing a variable number of items. 
Each customer has a certain patience. It waits to get to the counter until she’s at the end of her tether. If she gets to the counter, she uses it for a while before releasing it.

The scenario is so implemented with SimPype:

.. literalinclude:: ../../../examples/scenarios/supermarket.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/scenarios/log/supermarket/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/scenarios/log/supermarket/run01/sim.log
