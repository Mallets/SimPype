.. _queue:

================
Queue's behavior
================

The queue behavior of a given pipe can be customized in case of more complex queueing operations are needed
in addition to the simple FIFO buffer.
With this purpose, two decorators can be used to determine the `push` and `pop` behavior of the queue.
The two decorators are ``@simpype.queue.push`` and ``@simpype.queue.pop`` (see :func:`~simpype.queue.push` and :func:`~simpype.queue.pop` for more details).
There are two ways of customizing the behavior of a queue:

 * Work directly on the simulation scenario and perform an `inline customization`;
 * Create a `queue model` to be included in the simulation scenario through a custom `pipe model`.

Either approaches are valid, however `inline customization` is more suited for small customizations while `queue model` is
more suited for larger customizations and code re-usability (you can include the smae model multiple times in different simulations).

Inline customization
--------------------

In this example, a LIFO discipline is implemented.

.. code-block :: python

   import simpype
   import random

   sim = simpype.Simulation(id = 'simple')
   gen0 = sim.add_generator(id = 'gen0')
   gen0.message.property['priority'] = {
       0: lambda: random.randint(0,1)
   }
   res0 = sim.add_resource(id = 'res0')
   res0.pipe.add_queue(id = 'lifo')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   @simpype.pipe.enqueue(res0.pipe)
   def enqueue(self, message):
       return self.queue['lifo'].push(message)

   @simpype.pipe.dequeue(res0.pipe)
   def dequeue(self):
       return self.queue['lifo'].pop()

   @simpype.queue.push(res0.pipe.queue['lifo'])
   def push(self, message):
       return self.buffer.append(message)

   @simpype.queue.pop(res0.pipe.queue['lifo'])
   def pop(self):
       return self.buffer.pop(-1)

   sim.run(until = 10)

Custom model
------------

Alternatively, a separate `pipe model` and `queue model` can be created to implement the same discipline:

1. Edit ``mylifo.py`` with a text editor and create a pipe model in the following way:

.. code-block :: python

    import simpype

    class MyQueue(simpype.Queue):
        def __init__(self, sim, pipe, id):
            super().__init__(sim, pipe, id)
       
       @simpype.queue.push
       def push(self, message):
           return self.buffer.append(message)

       @simpype.queue.pop
       def pop(self):
           return self.buffer.pop(-1)


    class MyPipe(simpype.Pipe):
        def __init__(self, sim, resource, id):
            super().__init__(sim, resource, id)
            self.add_queue(id = 'lifo', model = 'mylifo')
       
        @simpype.pipe.enqueue
        def enqueue(self, message):
            return self.queue['lifo'].push(message)

        @simpype.pipe.dequeue
        def dequeue(self):
            return self.queue['lifo'].pop()

    # Do NOT remove. This is required for SimPype to build your model.
    queue = lambda *args: MyQueue(*args)
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
   res0 = sim.add_resource(id = 'res0', pipe = 'mylifo')
   res0.random['service'] = {
       0: lambda: 2.0
   }

   sim.run(until = 10)

3. Make sure that the file and directory structure is the following: 

.. code-block :: none

    <working directory>
    |-- simple.py 
    |-- mylifo.py

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
    |-- mylifo.py
