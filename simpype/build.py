"""
SimPype's build library.

"""

import importlib
import logging
import os


def _import(model, prefix):
	""" Dynamically import files given a path and a model.

	This functions imports a python source file as python model.

	Args:
		model (str):
			The name of the file to import withouth .py extension
		prefix (str):
			The path where the model is stored

	Returns:
		user-defined python module
	"""
	module = importlib.machinery.SourceFileLoader(model, os.path.join(prefix, model+'.py')).load_module()
	return module

def logger(name, path):
	""" Create a logger object.

	This function creates a logger object for logging the simulation results.
	A logger accepts a (str) as input and writes it to the log file.

	Args:
		name (str):
			The name of the logger
		path (str):
			The path of the log file managed by the logger

	Returns:
		Python Logger from logging module :class:`logging.Logger`
	"""
	# Create a logger
	logger = logging.getLogger(path)
	logger.setLevel(logging.INFO)
	# Create a file handler
	# delay = True does not create the logging file if nothing is written
	fh = logging.FileHandler(path, mode = 'w', delay = True)
	# Define the format of the messages to be logged
	formatter = logging.Formatter('%(message)s')
	fh.setFormatter(formatter)
	# Add the file handler to the logger
	logger.addHandler(fh)
	return logger

def resource(sim, id, model = None, capacity = 1, pipe = None):
	""" Create a :class:`~simpype.resource.Resource` object.

	Dynamically build a resource object based on the model.
	If model is None the default resource model is built.

	Args:
		sim (:class:`~simpype.simulation.Simulation`): 
			The SimPype simulation object
		id (str):
			The resource id to build
		model (str, optional):
			The model of the resource
		capacity (int, optional):
			The capacity of the resource
		pipe (str, optional):
			The model of the pipe associated to the resource

	Returns:
		:class:`~simpype.resource.Resource`
	"""
	if model is None:
		module = importlib.import_module('simpype.model.resource')
	else:
		module = _import(model, sim.model.dir)
	return module.resource(sim, id, capacity, pipe)

def generator(sim, id, model = None):
	""" Create a :class:`~simpype.resource.Resource` object implementing a generator.

	Dynamically build a generator object based on the model.
	If model is None the default generator model is built.

	Args:
		sim (:class:`~simpype.simulation.Simulation`): 
			The SimPype simulation object
		id (str):
			The resource id to build
		model (str, optional):
			The model of the resource

	Returns:
		:class:`~simpype.resource.Resource`
	"""
	if model is None:
		module = importlib.import_module('simpype.model.generator')
	else:
		module = _import(model, sim.model.dir)
	return module.resource(sim, id)

def pipe(sim, resource, id, model = None):
	""" Create a :class:`~simpype.pipe.Pipe` object.

	Dynamically build a pipe object based on the model.
	If model is None the default pipe model is built.

	Args:
		sim (:class:`~simpype.simulation.Simulation`): 
			The SimPype simulation object
		resource (:class:`~simpype.resource.Resource`):
			The resource object this pipe is associated to
		id (str):
			The pipe id to build
		model (str, optional):
			The model of the pipe

	Returns:
		:class:`~simpype.pipe.Pipe`
	"""
	if model is None:
		module = importlib.import_module('simpype.model.pipe')
	else:
		module = _import(model, sim.model.dir)
	return module.pipe(sim, resource, id)

def queue(sim, pipe, id, model = None):
	""" Create a :class:`~simpype.queue.Queue` object.

	Dynamically build a queue object based on the model.
	If model is None the default queue model is built.

	Args:
		sim (:class:`~simpype.simulation.Simulation`): 
			The SimPype simulation object
		pipe (:class:`~simpype.pipe.Pipe`):
			The pipe object this queue is associated to
		id (str):
			The queue id to build
		model (str, optional):
			The model of the queue

	Returns:
		:class:`~simpype.queue.Queue`
	"""
	if model is None:
		module = importlib.import_module('simpype.model.queue')
	else:
		module = _import(model, sim.model.dir)
	return module.queue(sim, pipe, id)
