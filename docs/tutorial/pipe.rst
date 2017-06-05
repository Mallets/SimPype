.. _pipe:

===============
Pipe's behavior
===============

The pipe behavior of a given resource can be customized in case of more complex queueing operations are needed
in addition to the simple FIFO discipline.
With this purpose, multiple queueus can be added to the pipe and two decorators can be used to determine the 
`enqueueing` and `dequeueing` behavior of the pipe.
The two decorators are ``@simpype.pipe.enqueue`` and ``@simpype.pipe.dequeue`` (see :func:`~simpype.pipe.enqueue` and :func:`~simpype.pipe.dequeue` for more details).
There are two ways of customizing the behavior of a pipe:

 * Work directly on the simulation scenario and perform an `inline customization`;
 * Create a `pipe model` to be included in the simulation scenario.

Either approaches are valid, however `inline customization` is more suited for small customizations while `pipe model` is
more suited for larger customizations and code re-usability (you can include the smae model multiple times in different simulations).

Inline customization
--------------------

In this example, a priority queue with two service classes is implemented.

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['priority'] = {
       0: lambda: random.randint(0,1)
   }
   res0 = sim.add_resource(id = 'res0')
   res0.pipe.add_queue('slow')
   res0.pipe.add_queue('fast')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   @simpype.pipe.enqueue(res0.pipe)
   def enqueue(self, message):
       if message.property['priority'] == 0:
           return self.queue['slow'].push(message)
       elif message.property['priority'] == 1:
           return self.queue['fast'].push(message)
       else:
           return message.drop('unsupported priority')

   @simpype.pipe.dequeue(res0.pipe)
   def dequeue(self):
       if len(self.queue['fast']) > 0:
           return self.queue['fast'].pop()
       elif len(self.queue['slow']) > 0:
           return self.queue['slow'].pop()
       else
           return None

   sim.run(until = 10)

Custom model
------------

Alternatively, a separate `pipe model` can be created to implement the same pipe behavior:

1. Edit ``mypipe.py`` with a text editor and create a pipe model in the following way:

.. code-block :: python

    import simpype

    class MyPipe(simpype.Pipe):
        def __init__(self, sim, resource, id):
            super().__init__(sim, resource, id)
            self.add_queue(id = 'slow')
            self.add_queue(id = 'fast')
       
       @simpype.pipe.enqueue
       def enqueue(self, message):
           if message.property['priority'] == 0:
               return self.queue['slow'].push(message)
           elif message.property['priority'] == 1:
               return self.queue['fast'].push(message)
           else:
               return message.drop('unsupported priority')

       @simpype.pipe.dequeue
       def dequeue(self):
           if len(self.queue['fast']) > 0:
               return self.queue['fast'].pop()
           elif len(self.queue['slow']) > 0:
               return self.queue['slow'].pop()
           else
               return None

    # Do NOT remove. This is required for SimPype to build your model.
    pipe = lambda *args: MyPipe(*args)    

2. Create your simulation scenario including the new model:

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['priority'] = {
       0: lambda: random.randint(0,1)
   }
   res0 = sim.add_resource(id = 'res0', pipe = 'mypipe')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   sim.run(until = 10)

3. Make sure that the file and directory structure is the following: 

.. code-block :: none

    <working directory>
    |-- simple.py 
    |-- mypipe.py

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
    |-- mypipe.py
