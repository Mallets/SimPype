.. _example_bank_renege:

===========
Bank renege
===========

SimPype features used in this example: `Message lifetime <../tutorial/message.html#lifetime>`_.

The scenario of the simulation is the classical bank renege:

.. code-block:: none

   |Customer| -> |Counter|

This is example is taken from `SimPy <http://simpy.readthedocs.io/en/latest/examples/bank_renege.html>`_.
This example models a bank counter and customers arriving t random times. Each customer has a certain patience. It waits to get to the counter until she’s at the end of her tether. If she gets to the counter, she uses it for a while before releasing it.

The scenario is so implemented with SimPype:

.. literalinclude:: ../../examples/bank.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/bank/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/bank/run01/sim.log
