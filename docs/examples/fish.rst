.. _example_fish_factory:

============
Fish factory
============

SimPype features used in this example: `Random variables <../tutorial/random.html>`_, `Resource inline customization <../tutorial/resource.html#inline-customization>`_, `Message next <../tutorial/message.html#next>`_, `Log custom message properties <../tutorial/logging.html#log-custom-message-properties>`_.

The scenario of the simulation is a food factory processing fish:

.. code-block:: none

                           /-> |Dry|
                          /
   |Fish| -> |Selector| -+---> |Can|
                          \
                           \-> |Grill|

There are three species of fish arriving at the factory: ``cod``, ``tuna``, and ``calamari``.
These species need first to be sperated and process accordingly.
Cod will be dried, tuna will be cut in chunks and put in a can, calamari will be grilled.

.. literalinclude:: ../../examples/fish.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/fish/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../examples/log/fish/run01/sim.log
