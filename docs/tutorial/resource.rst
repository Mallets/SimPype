.. _resource:

===================
Resource's behavior
===================

The resource behavior can be customized in case of more complex operations are needed
in addition to the simple random generated service time.
With this purpose, the decorator ``@simpype.resource.service`` can be used (see :func:`~simpype.resource.service` for more details).
There are two ways of customizing the behavior of your resource:

 * Work directly on the simulation scenario and perform an `inline customization`;
 * Create a `resource model` to be included in the simulation scenario.

Either approaches are valid, however `inline customization` is more suited for small customizations while `resource model` is
more suited for larger customizations and code re-usability (you can include the smae model multiple times in different simulations).

Inline customization
--------------------

In this example, the service time of the resource also depends on the message property value ``wait``.

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['wait'] = {
       0: lambda: random.uniform(0,1)
   }
   res0 = sim.add_resource(id = 'res0')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   @simpype.resource.service(res0)
   def service(self, message):
       # Wait for a random time
       yield self.env.timeout(self.random['service'])
       # Wait for a time as reported in the message property
       yield self.env.timeout(message.property['wait'].value)

   sim.run(until = 10)

Custom model
------------

Alternatively, a separate `resource model` can be created to implement the same resource behavior:

1. Edit ``myresource.py`` with a text editor and create a resource model in the following way:

.. code-block :: python
    
    import simpype

    class MyResource(simpype.Resource):
       def __init__(self, sim, id, capacity = 1, pipe = None):
           super().__init__(sim, id, capacity, pipe)
                        
       @simpype.resource.service
       def service(self, message):
           # Wait for a random time
           yield self.env.timeout(self.random['service'])
           # Wait for a time as reported in the message property
           yield self.env.timeout(message.property['wait'].value)


    # Do NOT remove. This is required for SimPype to build your model.
    resource = lambda *args: MyResource(*args)

2. Create your simulation scenario including the new model:

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['wait'] = {
       0: lambda: random.uniform(0,1)
   }
   res0 = sim.add_resource(id = 'res0', model = 'myresource')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   sim.run(until = 10)

3. Make sure that the file and directory structure is the following: 

.. code-block :: none

    <working directory>
    |-- simple.py 
    |-- myresource.py

4. If you want to change the directory where SimPype looks for custom models, set the following variable in the simulation environment:

.. code-block :: python

   import simpype

   sim = simpype.Simulation(id = 'simple')
   sim.model.dir = '<your model dir>'

Please make sure you have reading permissions for ``<your model dir>``. 
In this case, the file and directory structure would look like:

.. code-block :: none

    <working directory>
    |-- simple.py 
    
    <your model dir>
    |-- myresource.py
