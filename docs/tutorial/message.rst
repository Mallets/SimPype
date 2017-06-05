.. _message:

====================
Message's operations
====================

Messages are the units processed by the resources and can store arbitrary information, called `properties` in SimPype.
Message properties can be of any values, including :class:`~simpype.random.Random` objects (see :ref:`random`).
See :class:`~simpype.message.Message` for a detailed API reference.

.. code-block :: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    gen0 = sim.add_generator(id = 'gen0')
    gen0.message.property['rand_prop'] = {
        # Every message generated between t=0 and t=10 will have 
        # the 'test' property value equal to 3.0
        0 : lambda: 3.0,
        # Every message generated between t=10 and t=20 will have
        # the 'test' property uniformly distributed between 2.5 and 3.5
        10: lambda: random.uniform(2.5, 3.5),
        # Every message generated between t=20 and t=inf will have 
        # the 'test' property exponentially distributed with lambda 0.20
        20: lambda: random.expovariate(0.20)
    }
    # Store the property as normal dictionary if no lambda functions is present
    gen0.message.property['dict_prop'] = {
        'a': 'avalue',
        'b': 'bvalue',
    }
    gen0.message.property['str_prop'] = 'mystr'
    gen0.message.property['int_prop'] = 3
    gen0.message.property['float_prop'] = 3.0
    # You can also store objects
    e = sim.env.event()
    gen0.message.property['event_prop'] = e

Please note that in this case there is no need of calling the ``simpype.Random`` constructor.
The message object automatically converts the dictionary into a :class:`~simpype.random.Random` object.
Please also note that property values can be randomly generated, nevertheless once they are generated they will always return the same value unless an explicit refresh is called

.. code-block :: python

   message.property['test'].refresh()

Drop
====

A message can be suddenly dropped by calling the function :meth:`~simpype.message.Message.drop`:

.. code-block :: python

   message.drop(id = 'bad luck')

In addition, a message can be dropped upon the occurence of a given event:

.. code-block :: python

   # Create a SimPy event
   e = sim.env.event()
   # Subscribe the dropping of the message to the event e
   message.drop(id = 'event bad luck', event = e)
   # Trigger the event
   e.succeed()
   # The message has now been dropped

The message is dropped only when the event ``e`` is triggered, that is `succeed` in SimPy notation.

Lifetime
========

A `lifetime` can be assigned to generated messages in the following way:

.. code-block :: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    gen0 = sim.add_generator(id = 'gen0')
    gen0.message.property['lifetime'] = {
        0: lambda: random.expovariate(0.20)
    }

The message is dropped when the `lifetime` expires.
To remove any `lifetime` from the message, use the following function:

.. code-block :: python

   message.unsubscribe(id = 'lifetime')


Event subscription
==================

A message can be susbscribed to a given event and a custom function can be executed upong event triggering, e.g.:

.. code-block :: python

    import simpype
    import random

    sim = simpype.Simulation(id = 'simple')
    gen0 = sim.add_generator(id = 'gen0')
    res0 = sim.add_resource(id = 'res0')
    res1 = sim.add_resource(id = 'res1')

    e = sim.env.event()
    def c(message, value):
        # Value of the event, e.g. 'OK'
        message.property['myevent'] = value

    @simpype.resource.service(res0)
    def service(self, message):
        global e
        # Trigger the event
        e.succeed(value = 'OK')
        e = sim.env.event()

    @simpype.resource.service(res1)
    def service(self, message):
        # Unsubscribe from the event
        message.unsubscribe(id = 'mysub')

    gen0.message.subscribe(event = e, callback = c, id = 'mysub')

The callback function must be defined according to the following format:

.. code-block :: python

   def callback(message, value):
       ... your code here ...
