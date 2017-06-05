========
Overview
========

SimPype is a simulation framework based on `SimPy <http://simpy.readthedocs.io>`_ that relies on the concepts of resource and pipe.
SimPype decouples the resource from its queue (pipe) in such a way multiple queueing techniques can be used with the same resource.
SimPype also allows to create both custom resource and pipe models that can be reused in multiple simulations.

SimPype supports only Python >= 3.3. Previous versions of pythons are not supported.
The quickest way to install SimPype is through `pip`: 

.. code-block :: bash
  $ pip3 install simpype

SimPype documentation can be found on `ReadTheDocs <http://simpype.readthedocs.io>`_.
SimPype repository is available on `GitHub <https://github.com/Mallets/SimPype>`_.

Concept
=======
