"""
SimPype's simulation.

.. code-block :: python

	# Import SimPype module
	import simpype
	# Import python random module
	import random

	# [Mandatory] Create a SimPype simulation object
	sim = simpype.Simulation(id = 'simple')
	# [Optional] Fix the seed for the pseudo-random generator
	sim.seed = 42
	# [Optional] Configure the log directory. 
	# [Default] Log are stored by default in the 'current working directory/log'
	sim.log.dir = 'mylog'

	# [Mandatory] Add at least one generator to the simulation
	gen0 = sim.add_generator(id = 'gen0')
	# [Mandatory] Assign an arrival time
	# Generator.random is a custom dictionary accepting the following format as values:
	# generator.random[<some_id>] = {
	# 	<initial_time> : lambda: <value>/<random_function>
	#	...
	# }
	# Random values can be generated in the following way:
	# 	generator.random[<some_id>].value
	# The random value is:
	# 	<value>/<random_function> the simulation time is equal or 
	# greater than (>=) <initial_time>, 0 otherwise
	gen0.random['arrival'] = {
		# From t=0 to t=10, arrival is constant every 3s
		0	: lambda: 3.0,
		# From t=10 to t=20, arrival is uniform between 2.5 and 3.5
		10	: lambda: random.uniform(2.5, 3.5),
		# From t=20 to t=inf, arrival is expovariate with lambda 0.20
		20	: lambda: random.expovariate(0.20)
	}

	# [Mandatory] Add at least one resource to the simulation
	res0 = sim.add_resource(id = 'res0')
	# [Mandatory] Assign a service time
	# Resource.random is a dictionary accepting the same Generator.random format
	res0.random['service'] = {
		# From t=0 to t=10, service is constant at 1.5s
		0	: lambda: 1.5,
		# From t=10 to t=20, service is uniform between 1.5 and 2.5
		10	: lambda: random.uniform(1.5, 2.5),
		# From t=20 to t=inf, arrival is expovariate with lambda 2.0
		20	: lambda: random.expovariate(2.0)
	}

	# [Mandatory] Add a pipeline connecting the generator and the resource
	p0 = sim.add_pipeline(gen0, res0)

	# [Mandatory] Run the simulation e.g. until t=30
	#             sim.run calls Simpy's env.run
	#             Any arg passed to sim.run is then passed to env.run
	sim.run(until = 30)


The log directory structure is the following:

.. code-block :: none

	log.dir
	|-- <simulation #1>
	|   |-- <run #1>
	|   |   |-- sim.cfg
	|   |   `-- sim.log
	|   |-- <run #2>
	|   |   |-- sim.cfg
	|   |   `-- sim.log
	|-- <simulation #2>
	|   |-- <run #1>
	|   |   |-- sim.cfg
	|   |   `-- sim.log
	|   |-- <run #2>
	|   |   |-- sim.cfg
	|   |   `-- sim.log
	|   ...
	...


``sim.cfg`` contains information about the simulation environment and has the following format:

.. code-block :: none

	Simulation Seed: 42
	Simulation Time: 30.000000000
	Execution Time: 0.003298451

``sim.log`` contains the actual log of the simulation events and has the following format:

.. code-block :: none

	timestamp,message,seq_num,resource,event
	0.000000000,gen0,0,res0,pipe.in
	0.000000000,gen0,0,res0,pipe.out
	1.500000000,gen0,0,res0,resource.serve
	3.000000000,gen0,1,res0,pipe.in
	3.000000000,gen0,1,res0,pipe.out
	4.500000000,gen0,1,res0,resource.serve
	6.000000000,gen0,2,res0,pipe.in
	6.000000000,gen0,2,res0,pipe.out
	7.500000000,gen0,2,res0,resource.serve
	9.000000000,gen0,3,res0,pipe.in
	9.000000000,gen0,3,res0,pipe.out
	10.500000000,gen0,3,res0,resource.serve
	12.000000000,gen0,4,res0,pipe.in
	12.000000000,gen0,4,res0,pipe.out
	13.525010755,gen0,4,res0,resource.serve
	15.139426798,gen0,5,res0,pipe.in
	15.139426798,gen0,5,res0,pipe.out
	16.862637537,gen0,5,res0,resource.serve
	17.914456117,gen0,6,res0,pipe.in
	17.914456117,gen0,6,res0,pipe.out
	20.091155604,gen0,6,res0,resource.serve
	21.150927331,gen0,7,res0,pipe.in
	21.150927331,gen0,7,res0,pipe.out
	21.196403533,gen0,7,res0,resource.serve

"""
import copy
import datetime
import functools
import inspect
import os
import random
import shutil
import simpy
import time

import simpype
import simpype.build


class Model:
	""" Class storing the simulation parameters regarding the dynamic models.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
	
	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.

	"""
	def __init__(self, sim):
		assert isinstance(sim, Simulation)
		self.sim = sim
		self.env = sim.env
		self.dir = os.getcwd()
	
	@property
	def dir(self):
		""" The folder containing the customs models to be loaded by the SimPype simulation environment. """
		return self._dir

	@dir.setter
	def dir(self, val):
		self._dir = os.path.abspath(val)


class Log:
	""" Class storing the simulation parameters regarding the dynamic models.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
	
	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		date (datetime.now()):
			The real world creation time of the simulation environment.
		file (bool):
			Write the logs to a file if ``True``. Default value is ``True``.
		print(bool):
			Print the logs to the console if ``True``. Default value is ``False``.

	"""
	def __init__(self, sim):
		assert isinstance(sim, Simulation)
		self.sim = sim
		self.env = sim.env
		self.date = datetime.datetime.now()
		self.dir = os.path.join(os.getcwd(), 'log')
		self.file = True
		self.print = False
		self._h_fixed = ["timestamp", "message", "seq_num", "resource", "event"]
		self._h_property = []
		self._first = True

	@property
	def dir(self):
		""" The folder where the simulation logs are written. """
		return self._dir

	@dir.setter
	def dir(self, val):
		self._dir = functools.reduce(os.path.join,[val, self.sim.id, str(self.date)])

	def _write_log(self, timestamp):
		assert isinstance(timestamp, simpype.message.Timestamp)
		s = ""
		if self._first:
			s = s + ",".join(self._h_fixed + self._h_property) + "\n"
			self._first = False
		s = s + "%.9f" % timestamp.timestamp + "," + timestamp.message.id + "," + \
			str(timestamp.message.seq_num) + "," + timestamp.resource.id + "," + timestamp.description
		for h in self._h_property:
			if h not in timestamp.message.property:
				timestamp.message.property[h] = 'NA'
			p = timestamp.message.property[h]
			p = "%.9f" % p if isinstance(p, float) else str(p.value)
			s = s + "," + p
		if self.file:
			self._log.info(s)
		if self.print:
			print(s)
	
	def _write_cfg(self, entry):
		if self.file:
			self._cfg.info(str(entry))
		if self.print:
			print(str(entry))

	def init(self):
		""" Initialize the log folder and the simulation loggers. """
		if self.file:
			if not os.path.exists(self.dir):
				os.makedirs(self.dir)
			self._log = simpype.build.logger('log', os.path.join(self.dir, 'sim.log'))
			self._cfg = simpype.build.logger('cfg', os.path.join(self.dir, 'sim.cfg')) 

	def write(self, entry):
		""" Write a log entry.
			
		Args:
			entry (:class:`~simpype.message.Timestamp`)(str):
				The entry to be logged. If the entry is :class:`~simpype.message.Timestamp`

		"""
		if isinstance(entry, simpype.message.Timestamp):
			self._write_log(entry)
		else:
			self._write_cfg(entry)

	def property(self, property):
		""" Enable the logging of a message property.

		Args:
			property (str):
				The property to log.

		"""
		self._h_property.append(property)


class Simulation:
	""" Class implementing the SimPype's simulation environment.

	Args:
		id (str):
			The simulation environment id.
	
	Attributes:
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The simulation environment id.
		resource (dict):
			The dictionary storing all the :class:`~simpype.resource.Resource` objects of the simulation.
		generator (dict):
			The dictionary storing all the :class:`~simpype.resource.Resource` objects implementing generator functionalities of the simulation.
		pipeline (dict):
			The dictionary storing all the :class:`~simpype.pipeline.Pipeline` objects of the simulation.
		log (:class:`Log`):
			The log class storing the logging parameters.
		model (:class:`Model`):
			The model class storing the custom model parameters.

	"""
	def __init__(self, id):
		self.env = simpy.Environment()
		self.id = id
		self.resource = {}
		self.generator = {}
		self.pipeline = {}
		self.seed = hash(random.random())
		self.log = Log(self)
		self.model = Model(self)

	@property
	def seed(self):
		""" The seed of the pseudo-random number generator used by this simulation. """
		return self._seed
	
	@seed.setter
	def seed(self, num):
		self._seed = num
		random.seed(num)

	def _update_message(self, pipeline):
		# Add the pipeline to the messages in the new pipeline
		generator = set(pipeline.resource.keys()) & set(self.generator.keys())
		for id in generator:
			self.generator[id].message.pipeline = pipeline

	def add_generator(self, id, model = None):
		""" Add a :class:`~simpype.resource.Resource` implementing generator funcionalities to the simulation environment.

		Args:
			id (str):
				The generator id
			model (str):
				The model of the generator. If model is ``None``, the default model is used.

		Returns:
			:class:`~simpype.resource.Resource`

		"""
		assert id not in self.generator
		assert id not in self.resource
		generator = simpype.build.generator(self, id, model)
		self.generator[generator.id] = generator
		self.resource[generator.id] = generator
		return generator

	def add_pipeline(self, *args):
		""" Chain multiples :class:`~simpype.resource.Resource` or :class:`~simpype.pipeline.Pipeline` objects into a pipeline..

		Args:
			*args (:class:`~simpype.resource.Resource`)(:class:`~simpype.pipeline.Pipeline`):
				Create a pipeline by chaining 2 or more :class:`~simpype.resource.Resource` or :class:`~simpype.pipeline.Pipeline` objects.
		
		Returns:
			:class:`~simpype.pipeline.Pipeline`

		"""
		assert len(args) > 1
		id = len(self.pipeline)
		pipeline = simpype.Pipeline(self, id)
		for i in range(0, len(args)-1):
			src, dst = args[i], args[i+1]
			pipeline.add_pipe(src, dst)
		self._update_message(pipeline)
		self.pipeline[pipeline.id] = pipeline
		return pipeline
	
	def add_resource(self, id, model = None, capacity = 1, pipe = None):
		""" Add a :class:`~simpype.resource.Resource` object to the simulation environment. 
		
		Args:
			id (str):
				The resource id
			model (str):
				The model of the resource. If model is ``None``, the default model is used.
			capacity (int):
				The capacity of the resource, that is the number of :class:`~simpype.message.Message` objects that the resource can simultaneously serve.
			pipe (str):
				The model of the pipe associated to the resource. If model is ``None``, the default model is used.

		Returns:
			:class:`~simpype.resource.Resource`

		"""
		assert id not in self.resource
		resource = simpype.build.resource(self, id, model, capacity, pipe)
		self.resource[resource.id] = resource
		return resource

	def merge_pipeline(self, *args):
		""" Merge varioues :class:`~simpype.pipeline.Pipeline` objects into a single pipeline.

		Args:
			*args (:class:`~simpype.pipeline.Pipeline`):
				Create a pipeline by merging 2 or more :class:`~simpype.pipeline.Pipeline` objects.
		
		Returns:
			:class:`~simpype.pipeline.Pipeline`

		"""
		assert len(args) > 1
		id = len(self.pipeline)
		pipeline = simpype.Pipeline(self, id)
		for i in range(0, len(args)):
			pipeline.merge_pipe(args[i])
		self._update_message(pipeline)
		self.pipeline[pipeline.id] = pipeline
		return pipeline

	def run(self, *args, **kwargs):
		""" Run the simulation environment using SimPy environment. """
		self.log.init()
		sptime = time.process_time()
		self.env.run(*args, **kwargs)
		eptime = time.process_time()
		# Save some simulation parameters
		self.log.write("Simulation Seed: "+ str(self.seed))
		self.log.write("Simulation Time: " + "%.9f" % self.env.now)
		self.log.write("Execution Time: " + "%.9f" % (eptime - sptime))
