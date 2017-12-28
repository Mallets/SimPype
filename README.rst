.. image:: https://travis-ci.org/Mallets/SimPype.svg?branch=master
    :target: https://travis-ci.org/Mallets/SimPype

.. image:: https://codecov.io/gh/Mallets/SimPype/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Mallets/SimPype

.. image:: https://badge.fury.io/py/simpype.svg
    :target: https://badge.fury.io/py/simpype

.. image:: https://readthedocs.org/projects/simpype/badge/?version=latest
    :target: http://simpype.readthedocs.io/en/latest/?badge=latest

.. figure:: https://raw.githubusercontent.com/Mallets/SimPype/master/docs/_static/simpype_transparent.png
    :align: center
    :figwidth: 80 %


========
Overview
========

SimPype is a simulation framework based on `SimPy <http://simpy.readthedocs.io>`_ that relies on the concepts of resource and pipe.
SimPype decouples the resource from its queue (pipe) in such a way multiple queueing techniques can be used with the same resource.
SimPype also allows to create both custom resource and pipe models that can be reused in multiple simulations.

SimPype supports only Python >= 3.3. Previous versions of Python are not supported.
The quickest way to install SimPype is through `pip3`: 

    >>> pip3 install simpype

SimPype automatically installs SimPy as dependency.

SimPype documentation can be found on `ReadTheDocs <http://simpype.readthedocs.io>`_ while the source code repository is available on `GitHub <https://github.com/Mallets/SimPype>`_.

Scope
=====

SimPype is tailored to scenarios where the queueing disciplines and the resources occupation are key parts of the system under simulation.
People queueing at a post office, supermarket, car wash, cafeteria, etc. are examples of such scenarios.

Concept
=======

A SimPype simulation environment comprises at least one `generator` and one `resource` which are connected via a `pipeline`.
The generator generates `messages` with a given `arrival time`.
Those messages are firs enqueue in the resource `pipe` and next processed by the resources according with a `service time`.

A simple scenario with one generator and one resource can be defined as follows in a python3 console:

    >>> import simpype
    >>> import random
    >>> sim = simpype.Simulation(id = 'overview')
    >>> gen0 = sim.add_generator(id = 'gen0')
    >>> gen0.random['arrival'] = {0: lambda: random.expovariate(1.0)}
    >>> res0 = sim.add_resource(id = 'res0')
    >>> res0.random['service'] = {0: lambda: random.expovariate(2.0)}
    >>> p0 = sim.add_pipeline(gen0, res0)
    >>> sim.run(until = 10)

The simulation steps can be summarized as follows:

    1. The generator waits a ``random arrival time`` and generates a message;
    2. The generator ``sends the message`` to the resource;
    3. The ``message is enqueued`` in the resource's pipe;
    4. When the resource becomes available, the ``message is dequeued`` from the pipe;
    5. The ``message is served`` by the resource;
    6. The message leaves the resource after a ``random service time`` and is sent to the next resource (if any) - Go to step 3.

Any simulation steps can be customized as desired. Follows the `tutorial <http://simpype.readthedocs.io/en/latest/tutorial/index.html>`_ to learn how to customize your simulation environment.

SimPype also provides a built-in logging system for your simulation that automatically logs the simulation steps 3, 4, and 5.
The built-in system produces the logs in a tidy format where each variable is saved in its own column and each observation is saved in its own row:

    >>> timestamp,message,seq_num,resource,event
    ... 0.000000000,gen0,0,res0,pipe.in
    ... 0.000000000,gen0,0,res0,pipe.out
    ... 0.030509067,gen0,0,res0,resource.serve
    ... 4.283987797,gen0,1,res0,pipe.in
    ... 4.283987797,gen0,1,res0,pipe.out
    ... 4.296562508,gen0,1,res0,resource.serve
    ... 4.944812881,gen0,2,res0,pipe.in
    ... 4.944812881,gen0,2,res0,pipe.out
    ... 5.128244999,gen0,2,res0,resource.serve
    ... 6.402898951,gen0,3,res0,pipe.in
    ... 6.402898951,gen0,3,res0,pipe.out
    ... 7.044417615,gen0,3,res0,resource.serve
    ... 7.561061272,gen0,4,res0,pipe.in
    ... 7.561061272,gen0,4,res0,pipe.out
    ... 7.729431178,gen0,5,res0,pipe.in
    ... 8.129979622,gen0,4,res0,resource.serve
    ... 8.129979622,gen0,5,res0,pipe.out
    ... 8.171601538,gen0,6,res0,pipe.in
    ... 8.886733703,gen0,5,res0,resource.serve
    ... 8.886733703,gen0,6,res0,pipe.out
    ... 8.949540209,gen0,6,res0,resource.serve

This data format is well-suited for being directly processed by data manipulation tools like `pandas <http://pandas.pydata.org/>`_  or `dplyr <https://cran.rstudio.com/web/packages/dplyr/vignettes/introduction.html>`_. SimPype does not provide any tools for parsing the data. 
