.. _example_boarding_gate:

=============
Boarding gate
=============

SimPype features used in this example: `Random variables <../tutorial/random.html>`_, `Pipe custom model <../tutorial/pipe.html#custom-model>`_.

The scenario of the simulation is a boarding gate:

.. code-block:: none

   |First class|    \
                     \
   |Business class| --+-> |Boarding gate|
                     /
   |Economy class|  /

This simulation models a boarding gate for a flight with three separate classes: ``first``, ``business``, and ``economy``.
Boarding priority is given to the different classes according to the following order:

1. first class
2. business class
3. economy class

With ``first class`` having the highest priority and ``economy class`` having the lowest.
 
.. literalinclude:: ../../examples/boarding.py
   :language: python

Where pipe model ``p_priority`` is so implemented:

.. literalinclude:: ../../examples/model/p_priority.py

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/boarding/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/boarding/run01/sim.log
