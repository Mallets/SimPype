import copy
import datetime
import functools
import inspect
import os
import random
import shutil
import simpy
import time

import simpype.build
import simpype.message
import simpype.pipeline


class Model:
	def __init__(self, sim):
		assert isinstance(sim, Simulation)
		self.sim = sim
		self.env = sim.env
		self.dir = os.getcwd()
	
	@property
	def dir(self):
		return self._dir

	@dir.setter
	def dir(self, val):
		self._dir = os.path.abspath(val)


class Log:
	def __init__(self, sim):
		assert isinstance(sim, Simulation)
		self.sim = sim
		self.env = sim.env
		self.date = datetime.datetime.now()
		self.dir = os.path.join(os.getcwd(), 'log')
		self._h_fixed = ["timestamp", "message", "seq_num", "resource", "event"]
		self._h_property = []
		self._first = True

	@property
	def dir(self):
		return self._dir

	@dir.setter
	def dir(self, val):
		self._dir = functools.reduce(os.path.join,[val, self.sim.id, str(self.date)])

	def _write_log(self, timestamp):
		assert isinstance(timestamp, simpype.message.Timestamp)
		if self._first:
			self._log.info(",".join(self._h_fixed + self._h_property))
			self._first = False
		s = "%.9f" % timestamp.timestamp + "," + timestamp.message.id + "," + \
			str(timestamp.message.seq_num) + "," + timestamp.resource.id + "," + timestamp.event 
		for h in self._h_property:
			p = timestamp.message.property[h] if h in timestamp.message.property else 'NA'
			p = "%.9f" % p if isinstance(p, float) else str(p.value)
			s = s + "," + p
		self._log.info(s)
	
	def _write_cfg(self, entry):
		self._cfg.info(str(entry))

	def init(self):
		if not os.path.exists(self.dir):
			os.makedirs(self.dir)
		self._log = simpype.build.logger('log', os.path.join(self.dir, 'sim.log'))
		self._cfg = simpype.build.logger('cfg', os.path.join(self.dir, 'sim.cfg')) 

	def write(self, entry):
		if isinstance(entry, simpype.message.Timestamp):
			self._write_log(entry)
		else:
			self._write_cfg(entry)

	def property(self, property):
		self._h_property.append(property)


class Simulation:
	def __init__(self, id):
		assert isinstance(id, str)
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
		assert id not in self.generator
		assert id not in self.resource
		generator = simpype.build.generator(self, id, model)
		self.generator[generator.id] = generator
		self.resource[generator.id] = generator
		return generator

	def add_pipeline(self, *args):
		assert len(args) > 1
		id = len(self.pipeline)
		pipeline = simpype.pipeline.Pipeline(self, id)
		for i in range(0, len(args)-1):
			src, dst = args[i], args[i+1]
			pipeline.add_pipe(src, dst)
		self._update_message(pipeline)
		self.pipeline[pipeline.id] = pipeline
		return pipeline
	
	def add_resource(self, id, model = None, capacity = 1, pipe = None):
		assert id not in self.resource
		resource = simpype.build.resource(self, id, model, capacity, pipe)
		self.resource[resource.id] = resource
		return resource

	def merge_pipeline(self, *args):
		assert len(args) > 1
		id = len(self.pipeline)
		pipeline = simpype.pipeline.Pipeline(self, id)
		for i in range(0, len(args)):
			pipeline.merge_pipe(args[i])
		self._update_message(pipeline)
		self.pipeline[pipeline.id] = pipeline
		return pipeline

	def run(self, *args, **kwargs):
		self.log.init()
		sptime = time.process_time()
		self.env.run(*args, **kwargs)
		eptime = time.process_time()
		# Save some simulation parameters
		self.log.write("Simulation Seed: "+ str(self.seed))
		self.log.write("Simulation Time: " + "%.9f" % self.env.now)
		self.log.write("Execution Time: " + "%.9f" % (eptime - sptime))
