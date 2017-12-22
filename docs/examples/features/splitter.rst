.. _example_splitter:

========
Splitter
========

The scenario of the simulation is the following:

.. code-block:: none

                               /-> |Resource #0|
   |Generator| -> |Splitter| -(
                               \-> |Resource #1|

Where messages with even sequence number are sent to `Resource #0` and
messages with odd  sequence number are sent to `Resource #1` instead.
The scenario is so implemented with SimPype:

.. literalinclude:: ../../../examples/features/splitter.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/splitter/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/splitter/run01/sim.log
