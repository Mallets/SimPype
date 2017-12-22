.. _example_feature_arrival_service:

=========================================
Dynamic arrival and service distributions
=========================================

The scenario of the simulation is the following:

.. code-block:: none

   |Generator| -> |Resource|

The scenario is so implemented with SimPype:

.. literalinclude:: ../../../examples/features/arrival_service.py
   :language: python

``sim.cfg`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/arrival_service/run01/sim.cfg

``sim.log`` stored under the ``log`` folder contains:

.. literalinclude:: ../../../examples/features/log/arrival_service/run01/sim.log
