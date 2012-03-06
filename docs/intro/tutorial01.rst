====================================
Writing your first Vumi app - Part 1
====================================

This is the first part in a series of tutorials demonstrating how to develop Vumi apps.

In this tutorial we'll be developing a simple chat bot with which you can communicate via XMPP (in particular Google Talk).

We'll assume you have a working knowledge of Python_, RabbitMQ_ and VirtualEnv_.

.. admonition:: Where to get help:

    If you're having trouble at any point feel free to drop by #vumi_ on irc.freenode.net to chat with other Vumi users who might be able to help.

In this first part of the tutorial we'll be creating and testing a working environment. 

Environment Setup
=================

Before we proceed let's create an isolated working environment using VirtualEnv_.

From the command line ``cd`` into a directory were you'd like to store your code then run the following command::

    $ virtualenv --no-site-packages ve

This will create a ``ve`` directory where any libraries you install will go, thus isolating your environment.
Once the virtual environment has been created activate it by running ``. ve/bin/activate``.
   
.. note::

    For this to work VirtualEnv_ needs to be installed. You can tell it's installed by executing ``virtualenv`` from the command line. If that command runs successfully with no errors VirtualEnv_ is installed. If not you can install it by executing ``sudo pip install virtualenv`` from the command line.

Now that you created and activated the virtual environment install Vumi with the following command::
    
    $ pip install -e git+git://github.com/praekelt/vumi.git@develop#egg=vumi

.. note::

    This will install the development version of Vumi containing the latest-and-greatest features. Although the development branch is kept stable it is not recommended for production environments.

If this is your first Vumi application you need to take care of some initial RabbitMQ_ setup. Namely you need to add a ``vumi`` user and a ``develop`` virtual host and grant the required permissions. Vumi includes a script to do this for you which you can execute with the following command::
    
    $ sudo ./ve/src/vumi/utils/rabbitmq.setup.sh

.. note::

    Vumi workers communicate over RabbitMQ_ and requires it being installed and running. You can tell it's installed and its current status by executing ``sudo rabbitmq-server`` from the command line. If the command is not found you can install RabbitMQ by executing ``sudo apt-get install rabbitmq-server`` from the command line (assuming you are on a Debian based distribution).

Testing the Environment
=======================

Let's verify this worked. A Telnet worker and an echo application is included in Vumi which you can use to test your environment.

.. note::

    A complete Vumi instance consists of a *transport worker* and an *application worker* which are managed as seperate processes. A *transport worker* is responsible for sending messages to and receiving messages. An *application worker* processes messages from a transport worker and sends replies.

Start the Telnet transport worker by executing the following command::

    $ twistd -n start_worker --worker-class vumi.transports.telnet.TelnetServerTransport --set-option=transport_name:telnet --set-option=telnet_port:9010

This utilizes Twisted_ to start a Telnet process listening on port 9010. Specifically it uses Vumi's builtin ``TelnetServerTransport`` to handle communication with Telnet clients. Note that we specify ``telnet`` as the transport name when providing ``--set-option=transport_name:telnet``. When starting the *application worker* as described next the same name should be used, thus connecting the *transport worker* with the *application worker*.

.. note::

    A transport worker is responsible for sending messages to and receiving messages from users in the big wide world. For this example we are using a very simple transport that interacts with a user over telnet. Other transport mechanisms Vumi supports include SMPP, XMPP, Twitter, IRC, HTTP and a variety of mobile network aggregator specific messaging protocols. In subsequent parts of this tutorial we'll be using the XMPP transport to communicate over Google Talk.

.. _#vumi: irc://irc.freenode.net/vumi
.. _Python: https://python.org/
.. _RabbitMQ: https://www.rabbitmq.com/
.. _Twisted: https://twistedmatrix.com/trac/
.. _VirtualEnv: https://pypi.python.org/pypi/virtualenv
