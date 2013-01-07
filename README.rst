

.. -*- coding: utf-8 -*-

SEED
====

Concept
-------

Storage of **Extemporal Ensemble Device**

Organize commodity storage devices with minimum cost to build a loose-coupled system, which features dynamic metadata-manager/storage-server/client nodes, and fast deployment.

Design
------

All modules in one excutable, the depenencies are listed in Requirements_.

_`Requirements`
---------------

* tornado_ web server

Related Work
------------

Various Distributed File Systems: GFS_, HDFS_, Ceph_, `Tahoe-LAFS`_, `Storage@home`_

Author
======

`ShiZhan <http://shizhan.github.com/>`_ (c) 2012

.. _`Amazon S3`: http://docs.amazonwebservices.com/AmazonS3/2006-03-01/dev/Introduction.html
.. _tornado: http://www.tornadoweb.org/
.. _GFS: http://labs.google.com/papers/gfs.html
.. _HDFS: http://hadoop.apache.org/index.html
.. _Ceph: http://ceph.com/
.. _`Tahoe-LAFS`: https://tahoe-lafs.org/trac/tahoe-lafs
.. _`Storage@home`: http://cs.stanford.edu/people/beberg/Storage@home2007.pdf
