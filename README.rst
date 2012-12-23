

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

The interface is compatible with `Amazon S3`_.

_`Requirements`
---------------

* tornado_ web server
* s3 server (in tornado_ demo)

::

    curl https://raw.github.com/facebook/tornado/master/demos/s3server/s3server.py -o s3server.py

* s3 client

::

    curl https://raw.github.com/nephics/python-s3/master/s3/S3.py -o s3client.py

The hashlib module deprecates the separate md5 and sha modules, so the sha should be change to hashlib.sha1.

The `link <http://aws.amazon.com/code/134>`_ to original version seems to be broken.

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
