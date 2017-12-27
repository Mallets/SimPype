"""
:class:`~simpype.random.Random` is a custom dictionary accepting the following format as value:

.. code-block :: python

	sim = simpype.Simulation(id = 'test')
	myrand = simpype.Random(sim, {
		initial_time : lambda_function
		...
	})

Where each dictionary element is so defined:

	* ``initial_time`` is the element key and must be of *int* or *float* type. It represents the initial simulation time at which the ``lambda_function`` is invoked;
	* ``lambda_function`` is the element value. It is mandatory that for the value to be a *lambda* function. Such function must return a value, usually a *int* or a *float*;

An example of random dictionary initialization is the following:

.. code-block :: python

	sim = simpype.Simulation(id = 'test')
	myrand = simpype.Random(sim, {
		# From t=0 to t=10, the random variable returns 
		# the constant value of 3.0
		0	: lambda: 3.0,
		# From t=10 to t=20, the random variable returns 
		# value uniformly distributed between 2.5 and 3.5
		10	: lambda: random.uniform(2.5, 3.5),
		# From t=20 to t=inf, the random variable returns 
		# a value exponentially distributed with lambda 0.20
		20	: lambda: random.expovariate(0.20)
	})

A second example of random dictionary with generation interrupts is the following:

.. code-block :: python

	sim = simpype.Simulation(id = 'test')
	myrand = simpype.Random(sim, {
		# From t=0 to t=10, the random variable returns 
		# the constant value of 3.0 after time 10.
		# From time 0 to 10, no random variable is generated
		10	: lambda: 3.0,
		# From t=10 to t=20, no random variable is generated
		10	: lambda: None,
		# From t=20 to t=30, the random variable returns 
		# a value exponentially distributed with lambda 0.20
		20	: lambda: random.expovariate(0.20)
		# From t=30 to t=inf, no random variable is generated
		30	: lambda: None
	})

Produce a random value:

.. code-block :: python

	# Simulation time = 5.0
	random_value = myrand.value    # random_value = 3.0
	...
	# Simulation time = 15.0
	random_value = myrand.value    # random_value = 3.2476115513945767
	...
	# Simulation time = 25.0
	random_value = myrand.value    # random_value = 7.374759019459148

"""
import random

import simpype


class Random:
	""" SimPype's random class that may return different values depending on the simulation time.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		step_dict (dict):
			The dictionary storing the random steps.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		step_dict (dict):
			The dictionary storing the random steps.
		step_list (list):
			The list storing the sorted random steps.
	
	"""
	class Step:
		def __init__(self, tfrom, tto, process):
			self.tfrom = tfrom
			self.tto = tto
			self.process = process

	def __init__(self, sim, step_dict):
		assert isinstance(sim, simpype.Simulation)
		self.sim = sim
		self.env = sim.env
		self.step_dict = {}
		self.step_list = []
		# Init	
		for v in step_dict.values():
			assert callable(v)

		if 0 not in step_dict:
			step_dict[0] = lambda: None
		step_dict[float("inf")] = lambda: None
		time_step = sorted(step_dict)

		# Parse and build the steps
		i = 0
		while i < len(time_step)-1:
			tfrom = time_step[i]

			j = i+1
			while j < len(time_step):
				tto = time_step[j]
				a = step_dict[time_step[i]]
				b = step_dict[time_step[j]]

				create = True
				if a() is not None:
					process = a
					create = True
					# break
					i = i+1
					j = float("inf")
				elif a() is None and b() is not None:
					wait = (tto - tfrom) + b()
					process = lambda: wait
					create = True
					# break
					i = j
					j = float("inf")
				elif a() is None and b() is None:
					if j == len(time_step) - 1:
						process = b
						create = True
						# break
						i = float("inf")
						j = float("inf")
					else:
						j = j+1
					
				if create:
					s = self.Step(tfrom, tto, process)
					self.step_list.append(s)
					self.step_dict[s.tfrom] = s

	@property
	def value(self):
		""" Returns a random value given the current simulation time.

		Returns:
			Value as returned by the the ``lambda`` function.
			
		"""
		while self.step_list[0].tto <= self.env.now:
			self.step_list.pop(0)
		return self.step_list[0].process()


class RandomDict(dict):
	""" A custom dictionary storing :class:`Random` objects.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
	
	"""
	def __init__(self, sim):
		assert isinstance(sim, simpype.Simulation)
		super().__init__()
		self.sim = sim
		self.env = sim.env
	
	def __setitem__(self, key, value):
		if isinstance(value, Random):
			super().__setitem__(key, value)
		else:
			super().__setitem__(key, Random(self.sim, value))
