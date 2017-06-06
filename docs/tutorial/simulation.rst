.. _simulation:

=================
Simple simulation
=================

To build your first SimPype simulation, you simply need a console environment and a text editor.
Write the following block of code into a text file, e.g. ``simple.py``.

.. code-block:: python

	# [Mandatory] Import SimPype module
	import simpype
	import random

	# [Mandatory] Create a SimPype simulation object
	sim = simpype.Simulation(id = 'simple')

	# [Mandatory] Add at least one generator to the simulation
	gen0 = sim.add_generator(id = 'gen0')
	gen0.random['arrival'] = {
		0: lambda: random.expovariate(2.0)
	}

	# [Mandatory] Add at least one resource to the simulation
	res0 = sim.add_resource(id = 'res0')
	# [Mandatory] Assign a service time
	res0.random['service'] = {
		0: lambda: random.expovariate(3.0)
	}

	# [Mandatory] Add a pipeline connecting the generator to the resource
	p0 = sim.add_pipeline(gen0, res0)

	# [Mandatory] Run the simulation e.g. until t=5
	#             sim.run calls Simpy's env.run
	#             Any args passed to sim.run is then passed to env.run
	sim.run(until = 5)

Now run the simulation by typing the following command in the console:

.. code-block:: bash

    $ python3 simple.py

If your simulation name has a different name than ``simple.py``, just replace ``simple.py`` with ``your filename``.
SimPype automatically logs the simulation results, see :ref:`logging` for a detailed explaination on how to read the log files.
