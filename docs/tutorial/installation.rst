============
Installation
============

SimPype is a simulation framework based on `SimPy (>=3.0.10) <http://simpy.readthedocs.io>`_ and runs on Python 3 (>=3.3) only.
So make sure you have a recent version of Python installed on your system.
SimPype also supports PyPy for an easy distribution and installation. If you have `pip3 <http://pypi.python.org/pypi/pip>`_ installed, just type:

.. code-block:: bash

    $ pip3 install simpype

Please note that the command is called ``pip3`` and not simply ``pip``.
SimPy is automatically installed as dependency, so you do not need to install it manually.

If you don't have ``pip3`` installed on your system, you might install it with the following commands:

On Centos:

.. code-block :: bash

   $ yum install python34-pip

On Fedora:

.. code-block :: bash

   $ dnf install python3-pip

On Debian:

.. code-block :: bash

   $ apt-get install python3-pip

On Ubuntu:

.. code-block :: bash

   $ apt-get install python3-pip

For any other systems, please refer to their documentation.


Installing from source
======================

If you prefer installing SimPype from source, you have two options:

From PyPi
---------
You can `download SimPype <https://pypi.python.org/pypi/simpype/>`_
and install it manually. Extract the archive, open a terminal window where you
extracted SimPype and type:

.. code-block:: bash

    $ python3 setup.py install

From GitHub
-----------
Alternatively, you can clone `SimPype repository <https://github.com/Mallets/SimPype>`_ 
from `GitHub <https://github.com/>`_ by typing in a terminal windows:

.. code-block :: bash

    $ git clone https://github.com/Mallets/SimPype.git

Now change your working directory in the freshly cloned repository and type:

.. code-block:: bash

    $ python3 setup.py install
