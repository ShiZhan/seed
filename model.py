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

_core_model_file = 'seed.owl'
_node_model_file = 'node.owl'


class Model(Graph):
    """SEED Model Class"""
    def __init__(self):
        Graph.__init__(self)

    def create_header(self, base_uri):
        """create prefix, base and datatypes for base_uri"""
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

        self.add((self.base, RDF.type,     OWL.Ontology))
        self.add((self.base, RDFS.comment, Literal('SEED ontology', lang='EN')))
        self.add((self.base, DC.date,      Literal('2013-01-31')))
        self.add((self.base, DC.creator,   Literal('Shi.Zhan')))
        self.add((self.base, DC.created,   Literal(
            time.strftime(u'%Y-%m-%d %H:%M:%S'.encode('utf-8'),
            time.localtime(time.time())).decode('utf-8'))))
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
        self.add((self.base, OWL.versionInfo, Literal(VERSION,
            datatype=XSD.hexBinary)))

        # if in node model, import core model.
        if not (base_uri == _seed_base):
            self.add((self.base, OWL.imports, URIRef(_seed_base)))

        # setup datatype
        self.add((XSD.anyType, RDF.type, RDFS.Datatype))

    def set_property(self, (sub, pre, obj),
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
             # keep integrety, since onDataRange has been set.
            if (max_qc is None) and (min_qc is None):
                self.add((_node, OWL.qualifiedCardinality,
                    Literal(1, datatype=XSD.nonNegativeInteger)))

        self.add((sub, RDFS.subClassOf, _node))

