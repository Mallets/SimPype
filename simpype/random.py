import random

import simpype.simulation


class Random:
	class Step:
		def __init__(self, tfrom, tto, process):
			self.tfrom = tfrom
			self.tto = tto
			self.process = process

	def __init__(self, sim, step_dict):
		assert isinstance(sim, simpype.simulation.Simulation)
		self.sim = sim
		self.env = sim.env
		self.step_dict = step_dict
		self.step_list = []
		# Init		
		time_step = sorted(step_dict) + [float("inf")]
		if time_step[0] != 0:
			time_step = [0] + time_step
			step_dict[0] = lambda: 0
		for i in range(0, len(time_step)-1):
			self.step_list.append(self.Step(time_step[i], time_step[i+1], step_dict[time_step[i]]))

	@property
	def value(self):
		while self.step_list[0].tto <= self.env.now:
			self.step_list.pop(0)
		return self.step_list[0].process()


class RandomDict(dict):
	def __init__(self, sim):
		assert isinstance(sim, simpype.simulation.Simulation)
		super().__init__()
		self.sim = sim
		self.env = sim.env
	
	def __setitem__(self, key, value):
		if isinstance(value, Random):
			super().__setitem__(key, value)
		else:
			super().__setitem__(key, Random(self.sim, value))
