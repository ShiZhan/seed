.. -*- coding: utf-8 -*-

SEED
====

Concept
-------

Storage of **Extemporal Ensemble Device**

Organize commodity storage devices with minimum cost to build a loose-coupled system, which features dynamic metadata-manager/storage-server/client nodes, and fast deployment.

Design
------

Listed in Requirements_.

_`Requirements`
---------------

* Pyro_: a Python library (`MIT License <http://www.opensource.org/licenses/mit-license.php>`_) that helps building applications in which objects can talk to each other over the network. The code is in `SVN repository <http://svn.razorvine.net/Pyro/Pyro4>`_, use

::

    $ svn co svn://svn.razorvine.net/Pyro/Pyro4/trunk Pyro4.

to access.

.. _Pyro: http://packages.python.org/Pyro4/intro.html

This lib can be replace by xmlrpclib or some other rpc modules, if it's sufficiently lightweight and fast.

* RDFLib_: a Python library for working with RDF_, a simple yet powerful language for representing information.

Use

::

    $ pip install rdflib

or

::

    $ easy_install rdflib

to install, isodate_ may be installed automatically by pip.

.. _RDF: http://www.w3.org/RDF/
.. _RDFLib: https://github.com/RDFLib/rdflib
.. _isodate: https://github.com/gweis/isodate

Related Work
------------

Various Distributed File Systems: GFS_, HDFS_, Ceph_, `Tahoe-LAFS`_, `Storage@home`_

Author
======

`ShiZhan <http://shizhan.github.com/>`_ (c) 2012

.. _`Amazon S3`: http://docs.amazonwebservices.com/AmazonS3/2006-03-01/dev/Introduction.html
.. _GFS: http://labs.google.com/papers/gfs.html
.. _HDFS: http://hadoop.apache.org/index.html
.. _Ceph: http://ceph.com/
.. _`Tahoe-LAFS`: https://tahoe-lafs.org/trac/tahoe-lafs
.. _`Storage@home`: http://cs.stanford.edu/people/beberg/Storage@home2007.pdf
