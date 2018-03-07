.. _example_supermarket:

===========
Supermarket
===========

SimPype features used in this example: `Random variables <../tutorial/random.html>`_, `Resource inline customization <../tutorial/resource.html#inline-customization>`_, `Log custom message properties <../tutorial/logging.html#log-custom-message-properties>`_.

The scenario of the simulation is a supermaket:

.. code-block:: none

      |Mom| -\
              ) -> |Cashier|
   |Single| -/

This example models the last 4 hours of a normal working day of a supermarket.
There are two types of customer (``mom`` and ``single``) arriving at different times and purchasing a variable number of ``items`` each. 
The customers pay the goods at a cashier who takes a random service time for ``scanning the items`` and ``finalize the payment``.
The arrival time and the number of time vary depending on the hour for both types of customer.
Both customers cease to arrive at hour 4 because of the supermarket doors have been closed and no one is allowed to enter.
Nevertheless, customers already in the supermarket will do their grocery as usual.
Moreover, there are no single customers arriving between the 2nd and 3rd hour. 

The scenario is so implemented with SimPype:

.. literalinclude:: ../../examples/supermarket.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/supermarket/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/supermarket/run01/sim.log
