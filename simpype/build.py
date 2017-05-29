import importlib
import logging
import os


def _import(model, prefix):
	module = importlib.machinery.SourceFileLoader(model, os.path.join(prefix, model+'.py')).load_module()
	return module

def logger(name, path):
	# Create a logger
	logger = logging.getLogger(name)
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
	if model is None:
		module = importlib.import_module('simpype.model.resource')
	else:
		module = _import(model, sim.model.dir)
	return module.resource(sim, id, capacity, pipe)

def generator(sim, id, model = None):
	if model is None:
		module = importlib.import_module('simpype.model.generator')
	else:
		module = _import(model, sim.model.dir)
	return module.resource(sim, id)

def pipe(sim, resource, id, model = None):
	if model is None:
		module = importlib.import_module('simpype.model.pipe')
	else:
		module = _import(model, sim.model.dir)
	return module.pipe(sim, resource, id)

def queue(sim, pipe, id, model = None):
	if model is None:
		module = importlib.import_module('simpype.model.queue')
	else:
		module = _import(model, sim.model.dir)
	return module.queue(sim, pipe, id)
