"""
SimPype's pipeline.

"""

import simpype.resource
import simpype.simulation


class Pipeline:
	""" The pipeline connecting the various :class:`~simpype.resource.Resource` instances.

	Args:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		id (str):
			The pipeline id.

	Attributes:
		sim (:class:`Simulation`):
			The SimPype simulation object.
		env (simpy.Environment):
			The SimPy environment object.
		id (str):
			The pipeline id.
		resource (dict):
			The dictionary storing the connected resources in the form of adjency list.
		first (:class:`~simpype.resource.Resource`):
			The first resource of the pipeline.
		last (:class:`~simpype.resource.Resource`):
			The last resource of the pipeline.

	"""
	def __init__(self, sim, id):
		assert isinstance(sim, simpype.simulation.Simulation)
		self.sim = sim
		self.env = sim.env
		self.id = id
		self.resource = {}
		self.first = None
		self.last = None

	def add_pipe(self, src, dst):
		""" Add a pipe to the pipeline.
		
		Connect resource ``src`` to resource ``dst``.

		Args:
			src (:class:`~simpype.resource.Resource`):
				The source resource of the pipe.
			dst (:class:`~simpype.resource.Resource`):
				The destination resource of the pipe.

		"""
		assert isinstance(src, (simpype.resource.Resource, Pipeline))
		assert isinstance(dst, (simpype.resource.Resource, Pipeline))
		# Src check
		tsrc = src if isinstance(src, simpype.resource.Resource) else src.last
		# Dst check
		tdst = dst if isinstance(dst, simpype.resource.Resource) else dst.first
		# Create the list in the dictionary if does not exist
		if tsrc.id not in self.resource:
			self.resource[tsrc.id] = []
		# Add the element to the pipe dictionary
		self.resource[tsrc.id].append(tdst)
		# Merge the pipe if src is pipeline instance
		if isinstance(src, Pipeline):
			self.merge_pipe(src)
		# Merge the pipe if dst is pipeline instance
		if isinstance(dst, Pipeline):
			self.merge_pipe(dst)
		# Set the first element of the pipe
		if self.first is None:
			self.first = src if isinstance(src, simpype.resource.Resource) else src.first
		# Set the last element of the pipe
		self.last = dst if isinstance(dst, simpype.resource.Resource) else dst.last

	def merge_pipe(self, pipeline):
		""" Merge ``pipeline`` with this pipeline.

		Args:
			pipeline (:class:`Pipeline`):
				The pipeline to be merged with this pipeline.

		"""
		assert isinstance(pipeline, Pipeline)
		for key, value in pipeline.resource.items():
			if key not in self.resource:
				self.resource[key] = []
			self.resource[key] = self.resource[key] + list(set(value)-set(self.resource[key]))
