.. _random:

================
Random variables
================

SimPype comes with a custom random variable generation system that allows you to generate 
random values according to different random distributions depending on the current simulation time.
See :class:`~simpype.random.Random` for a detailed API reference.

.. code-block:: python

    import simpype

    sim = simpype.Simulation(id = 'test')
    myrand = simpype.Random(sim, {
        initial_time : lambda_function
        ...
    })

Where each dictionary element is so defined:

	* ``initial_time`` is the element key and must be of *int* or *float* type. It represents the initial simulation time at which the ``lambda_function`` is invoked;
	* ``lambda_function`` is the element value. It is mandatory that for the value to be a *lambda* function. Such function must return a value, usually a *int* or a *float*;

An example of random variable initialization is the following:

.. code-block:: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'test')
    myrand = simpype.Random(sim, {
        # From t=0 to t=10, the random variable returns 
        # the constant value of 3.0
        0    : lambda: 3.0,
        # From t=10 to t=20, the random variable returns 
        # value uniformly distributed between 2.5 and 3.5
        10    : lambda: random.uniform(2.5, 3.5),
        # From t=20 to t=inf, the random variable returns 
        # a value exponentially distributed with lambda 0.20
        20    : lambda: random.expovariate(0.20)
    })

To generate a random value:

.. code-block:: python

    # Simulation time = 5.0
    random_value = myrand.value    # random_value = 3.0
    ...
    # Simulation time = 15.0
    random_value = myrand.value    # random_value = 3.2476115513945767
    ...
    # Simulation time = 25.0
    random_value = myrand.value    # random_value = 7.374759019459148

As you can see, depending on the current simulation ``myrand.value`` returns a random value according to a different random distribution.

Generator arrival time
======================

The arrival time of a generator is described with a :class:`~simpype.random.Random` variable.

.. code-block:: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    gen0 = sim.add_generator(id = 'gen0')
    # Start generating events at a random simulation time
    gen0.random['arrival'] = {
		# From t=0 to t=10, the arrival time is constant to 3.0
		0	: lambda: 3.0,
		# From t=10 to t=20, the arrival time is uniformly distributed between 2.5 and 3.5
		10	: lambda: random.uniform(2.5, 3.5),
		# From t=20 to t=inf, the arrival time is exponentially distributed with lambda 0.20
		20	: lambda: random.expovariate(0.20)
    }

Please note that in this case there is no need of calling the ``simpype.Random`` constructor.
The generator object automatically converts the dictionary into a :class:`~simpype.random.Random` object.

Resource service time
=====================

The service time of a resource is described with a :class:`~simpype.random.Random` variable.

.. code-block:: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    res0 = sim.add_resource(id = 'res0')
    res0.random['arrival'] = {
		# From t=0 to t=10, the service time is constant to 3.0
		0	: lambda: 3.0,
		# From t=10 to t=20, the service time is uniformly distributed between 2.5 and 3.5
		10	: lambda: random.uniform(2.5, 3.5),
		# From t=20 to t=inf, the service time is exponentially distributed with lambda 0.20
		20	: lambda: random.expovariate(0.20)
    }

Please note that in this case there is no need of calling the ``simpype.Random`` constructor.
The resource object automatically converts the dictionary into a :class:`~simpype.random.Random` object.

Message property
================

A message property can be described with a a :class:`~simpype.random.Random` variable.

.. code-block:: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    gen0 = sim.add_generator(id = 'gen0')
    gen0.message.property['test'] = {
		# Every message generated between t=0 and t=10 will have the 'test' property value equal to 3.0
		0	: lambda: 3.0,
		# Every message generated between t=10 and t=20 will have the 'test' property uniformly distributed between 2.5 and 3.5
		10	: lambda: random.uniform(2.5, 3.5),
		# Every message generated between t=20 and t=inf will have the 'test' property exponentially distributed with lambda 0.20
		20	: lambda: random.expovariate(0.20)
    }

Please note that in this case there is no need of calling the ``simpype.Random`` constructor.
The message object automatically converts the dictionary into a :class:`~simpype.random.Random` object.
Please also note that property values can be randomly generated, nevertheless once they are generated they will always return the same value unless an explicit refresh is called

.. code-block:: python

   message.property['test'].refresh()
