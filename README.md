# SimPype #

[![Build Status](https://travis-ci.org/Mallets/SimPype.svg?branch=master)](https://travis-ci.org/Mallets/SimPype)
[![codecov](https://codecov.io/gh/Mallets/SimPype/branch/master/graph/badge.svg)](https://codecov.io/gh/Mallets/SimPype)
[![PyPI version](https://badge.fury.io/py/simpype.svg)](https://badge.fury.io/py/simpype)

SimPype is a simulation framework based on Simpy that relies on the concepts of resource and pipe.
SimPype decouples the resource from its queue (pipe) in such a way multiple queueing techniques can be used with the same resource.
SimPype also allows to create both custom resource and pipe models.

SimPype supports Python >= 3.3. Previous versions of pythons are not supported at the moment.
You can install SimPype using pip: 

	$ pip3 install simpype

Documentiation is still work in progress.
Some examples are available at: https://github.com/Mallets/SimPype/tree/master/examples 
