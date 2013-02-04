#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""model -- SEED model API"""

import time

from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import Namespace, ClosedNamespace, RDF, RDFS, OWL, XSD

from utils import VERSION


# http://dublincore.org/documents/dc-rdf/
_dc_uri      = 'http://purl.org/dc/elements/1.1/'
_dcterms_uri = 'http://purl.org/dc/terms/'
DC           = Namespace(_dc_uri)
TERMS        = Namespace(_dcterms_uri)

# use google sites as persistent URL
_seed_base   = 'https://sites.google.com/site/ontology2013/seed.owl'
_seed_uri    = _seed_base + '#'

SEED = ClosedNamespace(
    uri = URIRef(_seed_uri),
    terms =
        [
            "Object", "Bucket", "SimpleObject", "CompositeObject",
            "contain", "stripe", "replicate", "redundancy",
            "name", "path", "mode", "ctime", "mtime", "atime",
            "length", "size", "owner", "group", "host"
        ]
)

DEFAULT_CORE_MODEL = 'seed.owl'
DEFAULT_NODE_MODEL = 'node.owl'


class Model(Graph):
    """SEED Model Class"""
    def __init__(self):
        Graph.__init__(self)

    # helper methods for creating seed models
    def _gen_header(self, base_uri):
        """generate prefix, base and datatypes for model base_uri"""

        # setup prefix
        self.bind("rdf",   "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.bind("rdfs",  "http://www.w3.org/2000/01/rdf-schema#")
        self.bind("xsd",   "http://www.w3.org/2001/XMLSchema#")
        self.bind("owl",   "http://www.w3.org/2002/07/owl#")
        self.bind("dc",    _dc_uri)
        self.bind("terms", _dcterms_uri)
        self.bind("seed",  _seed_uri)

        # setup base URI
        self.base = URIRef(base_uri)

        # this is an OWL Ontology
        self.add((self.base, RDF.type,     OWL.Ontology))

        self.add((self.base, RDFS.comment, Literal('SEED ontology', lang='EN')))

        # Dublin Core Metadata
        self.add((self.base, DC.date,      Literal('2013-01-31')))
        self.add((self.base, DC.creator,   Literal('Shi.Zhan')))
        self.add((self.base, DC.created,
                    Literal(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())).encode('utf-8'),
                            datatype=XSD.dateTimeStamp)
                ))
        self.add((self.base, TERMS.license, Literal('Copyright 2013 Shi.Zhan.'
            ' Licensed under the Apache License, Version 2.0 (the "License");'
            ' you may not use this file except in compliance with the License.'
            ' You may obtain a copy of the License at\n\n'
            '   http://www.apache.org/licenses/LICENSE-2.0.\n\n'
            ' Unless required by applicable law or agreed to in writing,'
            ' software distributed under the License is distributed on'
            ' an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,'
            ' either express or implied. See the License for the specific language'
            ' governing permissions and limitations under the License.',
            datatype=XSD.string)))

        # use program version as model version, recording the origin of model.
        self.add((self.base, OWL.versionInfo,
            Literal(VERSION, datatype=XSD.hexBinary)))

        # if in node model, import core model.
        if not (base_uri == _seed_base):
            self.add((self.base, OWL.imports, URIRef(_seed_base)))

        # setup default datatype
        self.add((XSD.anyType, RDF.type, RDFS.Datatype))


    def _set_property(self, (sub, pre, obj),
        only=False, some=False, max_qc=None, min_qc=None):
        """set property with restriction on object"""

        _node = BNode()
        self.add((_node, RDF.type, OWL.Restriction))
        self.add((_node, OWL.onProperty, pre))
        if only:
            self.add((_node, OWL.allValuesFrom, obj))
        elif some:
            self.add((_node, OWL.someValuesFrom, obj))
        else:
            self.add((_node, OWL.onDataRange, obj))
            if max_qc is not None:
                self.add((_node, OWL.maxQualifiedCardinality,
                    Literal(max_qc, datatype=XSD.nonNegativeInteger)))
            if min_qc is not None:
                self.add((_node, OWL.minQualifiedCardinality,
                    Literal(min_qc, datatype=XSD.nonNegativeInteger)))
            # keep integrity, something must be set
            # since onProperty, onDataRange has been set
            if (max_qc is None) and (min_qc is None):
                self.add((_node, OWL.qualifiedCardinality,
                    Literal(1, datatype=XSD.nonNegativeInteger)))

        self.add((sub, RDFS.subClassOf, _node))


    def _gen_core(self):
        """generate core model"""

        # core model base, prefix and namespace

        self._gen_header(_seed_base)

        # declare classes

        self.add((SEED.Object, RDF.type, OWL.Class))
        self.add((SEED.Bucket, RDF.type, OWL.Class))
        self.add((SEED.Bucket, RDFS.subClassOf, SEED.Object))
        self.add((SEED.SimpleObject, RDF.type, OWL.Class))
        self.add((SEED.SimpleObject, RDFS.subClassOf, SEED.Object))
        self.add((SEED.CompositeObject, RDF.type, OWL.Class))
        self.add((SEED.CompositeObject, RDFS.subClassOf, SEED.SimpleObject))

        self.add((SEED.Bucket, OWL.disjointWith, SEED.SimpleObject))

        # declare and assign properties

        self.add((SEED.contain,    RDF.type, OWL.ObjectProperty))
        self.add((SEED.stripe,     RDF.type, OWL.ObjectProperty))
        self.add((SEED.replicate,  RDF.type, OWL.ObjectProperty))
        self.add((SEED.redundancy, RDF.type, OWL.ObjectProperty))

        self.add((SEED.name,      RDF.type, OWL.DatatypeProperty))
        self.add((SEED.path,      RDF.type, OWL.DatatypeProperty))
        self.add((SEED.mode,      RDF.type, OWL.DatatypeProperty))
        self.add((SEED.ctime,     RDF.type, OWL.DatatypeProperty))
        self.add((SEED.mtime,     RDF.type, OWL.DatatypeProperty))
        self.add((SEED.atime,     RDF.type, OWL.DatatypeProperty))
        self.add((SEED.length,    RDF.type, OWL.DatatypeProperty))
        self.add((SEED.size,      RDF.type, OWL.DatatypeProperty))
        self.add((SEED.owner,     RDF.type, OWL.DatatypeProperty))
        self.add((SEED.group,     RDF.type, OWL.DatatypeProperty))
        self.add((SEED.host,      RDF.type, OWL.DatatypeProperty))

        # Bucket contain only Object
        self._set_property((SEED.Bucket, SEED.contain, SEED.Object), only=True)

        # CompositeObject [stripe, replicate, redundancy] only SimpleObject
        self._set_property(
            (SEED.CompositeObject, SEED.stripe,     SEED.SimpleObject), only=True)
        self._set_property(
            (SEED.CompositeObject, SEED.replicate,  SEED.SimpleObject), only=True)
        self._set_property(
            (SEED.CompositeObject, SEED.redundancy, SEED.SimpleObject), only=True)

        # Object [name, mode, {c|m|a}time, length, size, owner, group]
        self._set_property((SEED.Object, SEED.name, XSD.normalizedString), max_qc=1)
        self._set_property((SEED.Object, SEED.mode, XSD.unsignedShort), max_qc=1)
        self._set_property((SEED.Object, SEED.ctime, XSD.unsignedLong), max_qc=1)
        self._set_property((SEED.Object, SEED.mtime, XSD.unsignedLong), max_qc=1)
        self._set_property((SEED.Object, SEED.atime, XSD.unsignedLong), max_qc=1)
        self._set_property((SEED.Object, SEED.size, XSD.unsignedLong), max_qc=1)
        self._set_property((SEED.Object, SEED.owner, XSD.unsignedShort), max_qc=1)
        self._set_property((SEED.Object, SEED.group, XSD.unsignedShort), max_qc=1)

        self._set_property((SEED.CompositeObject, SEED.size, XSD.unsignedLong), max_qc=1)

        # Object [host] only HOST_ID (8 Bytes)
        self._set_property((SEED.Object, SEED.host, XSD.hexBinary), only=True)

