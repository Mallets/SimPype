"""
The ``simpype`` module aggregates SimPype's most used components into a single
namespace. This is purely for convenience. You can of course also access
everything (and more!) via their actual submodules.

The following tables list all of the available components in this module.

{toc}

"""
from pkgutil import extend_path

from simpype.simulation import Simulation
from simpype.message import Message
from simpype.pipe import Pipe
from simpype.pipeline import Pipeline
from simpype.queue import Queue
from simpype.random import Random
from simpype.resource import Resource


def compile_toc(entries, section_marker='='):
	"""Compiles a list of sections with objects into sphinx formatted
	autosummary directives."""
	toc = ''
	for section, objs in entries:
		toc += '\n\n%s\n%s\n\n' % (section, section_marker * len(section))
		toc += '.. autosummary::\n\n'
		for obj in objs:
			toc += '	~%s.%s\n' % (obj.__module__, obj.__name__)
	return toc


toc = (
	('Simulation', (
		Simulation,
	)),
	('Resource', (
		Resource,
	)),
	('Pipe', (
		Pipe,
	)),
	('Pipeline', (
		Pipeline,
	)),
	('Queue', (
		Queue,
	)),
	('Message', (
		Message,
	)),
)

# Use the toc to keep the documentation and the implementation in sync.
if __doc__:
	__doc__ = __doc__.format(toc=compile_toc(toc))
__all__ = [obj.__name__ for section, objs in toc for obj in objs]

__path__ = extend_path(__path__, __name__)
__version__ = '1.1.0'
