#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""model -- SEED model definition, constant, API"""

import sys, os, time
from string import Template
from uuid import uuid1, getnode

from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import Namespace, ClosedNamespace, RDF, RDFS, OWL, XSD

from log import SEED_LOG
from util import VERSION
from netutil import DEFAULT_HOST


# BEGIN: model constants

# http://dublincore.org/documents/dc-rdf/
DC_URI      = 'http://purl.org/dc/elements/1.1/'
DC          = Namespace(DC_URI)
TERMS_URI   = 'http://purl.org/dc/terms/'
TERMS       = Namespace(TERMS_URI)

# use google sites as persistent URL
SEED_BASE   = 'https://sites.google.com/site/ontology2013/seed.owl'
SEED_URI    = SEED_BASE + '#'

SEED = ClosedNamespace(
    uri = URIRef(SEED_URI),
    terms =
        [
            "Object", "Bucket", "SimpleObject", "CompositeObject", "Root",
            "contain", "stripe", "replicate", "redundancy",
            "name", "origin",
            "mode", "ctime", "mtime", "atime", "length", "size", "uid", "gid"
        ]
)

DEFAULT_CORE_MODEL = 'seed.owl'
DEFAULT_NODE_MODEL = 'node.owl'

LICENSE = \
"""
Copyright 2013 Shi.Zhan.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing
permissions and limitations under the License.
"""

# END: model constants


def set_property(model, (sub, pre, obj),
    only=False, some=False, max_qc=None, min_qc=None):
    """
    set property with restriction on object
    in the form of 'sub' 'pre' {only|some|qualification} 'obj'
    """

    _node = BNode()
    model.add((_node, RDF.type, OWL.Restriction))
    model.add((_node, OWL.onProperty, pre))
    if only:
        model.add((_node, OWL.allValuesFrom, obj))
    elif some:
        model.add((_node, OWL.someValuesFrom, obj))
    else:
        model.add((_node, OWL.onDataRange, obj))
        if max_qc is not None:
            model.add((_node, OWL.maxQualifiedCardinality,
                Literal(max_qc, datatype=XSD.nonNegativeInteger)))
        if min_qc is not None:
            model.add((_node, OWL.minQualifiedCardinality,
                Literal(min_qc, datatype=XSD.nonNegativeInteger)))
        # keep integrity, something must be set
        # since onProperty, onDataRange has been set
        if (max_qc is None) and (min_qc is None):
            model.add((_node, OWL.qualifiedCardinality,
                Literal(1, datatype=XSD.nonNegativeInteger)))

    model.add((sub, RDFS.subClassOf, _node))


def gen_core():
    """generate SEED core model, the base import of all SEED node models."""

    SEED_LOG.info('creating core model ...')

    core = Graph()

    # core model base, prefix and namespace

    # setup prefix
    core.bind("rdf",   "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    core.bind("rdfs",  "http://www.w3.org/2000/01/rdf-schema#")
    core.bind("xsd",   "http://www.w3.org/2001/XMLSchema#")
    core.bind("owl",   "http://www.w3.org/2002/07/owl#")
    core.bind("dc",    DC_URI)
    core.bind("terms", TERMS_URI)
    core.bind("seed",  SEED_URI)

    # setup base URI
    core.base = URIRef(SEED_BASE)

    # this is an OWL Ontology
    core.add((core.base, RDF.type,     OWL.Ontology))

    core.add((core.base, RDFS.comment, Literal('SEED ontology', lang='EN')))

    # Dublin Core Metadata
    core.add((core.base, DC.date,      Literal('2013-01-31')))
    core.add((core.base, DC.creator,   Literal('Shi.Zhan')))
    core.add((core.base, DC.created,
                Literal(time.strftime('%Y-%m-%d %H:%M:%S',
                            time.localtime(time.time())).encode('utf-8'),
                        datatype=XSD.dateTimeStamp)
            ))
    core.add((core.base, TERMS.license, Literal(LICENSE, datatype=XSD.string)))

    # use program version as model version, recording the origin of model.
    core.add((core.base, OWL.versionInfo,
        Literal(VERSION, datatype=XSD.hexBinary)))

    # setup default datatype
    core.add((XSD.anyType, RDF.type, RDFS.Datatype))

    # declare classes

    core.add((SEED.Object, RDF.type, OWL.Class))
    core.add((SEED.Bucket, RDF.type, OWL.Class))
    core.add((SEED.Bucket, RDFS.subClassOf, SEED.Object))
    core.add((SEED.SimpleObject, RDF.type, OWL.Class))
    core.add((SEED.SimpleObject, RDFS.subClassOf, SEED.Object))
    core.add((SEED.CompositeObject, RDF.type, OWL.Class))
    core.add((SEED.CompositeObject, RDFS.subClassOf, SEED.SimpleObject))
    core.add((SEED.Root, RDF.type, OWL.Class))
    core.add((SEED.Root, RDFS.subClassOf, SEED.Bucket))

    core.add((SEED.Bucket, OWL.disjointWith, SEED.SimpleObject))

    # declare and assign properties

    core.add((SEED.contain,    RDF.type, OWL.ObjectProperty))
    core.add((SEED.stripe,     RDF.type, OWL.ObjectProperty))
    core.add((SEED.replicate,  RDF.type, OWL.ObjectProperty))
    core.add((SEED.redundancy, RDF.type, OWL.ObjectProperty))

    core.add((SEED.name,      RDF.type, OWL.DatatypeProperty))
    core.add((SEED.origin,    RDF.type, OWL.DatatypeProperty))

    core.add((SEED.mode,      RDF.type, OWL.DatatypeProperty))
    core.add((SEED.ctime,     RDF.type, OWL.DatatypeProperty))
    core.add((SEED.mtime,     RDF.type, OWL.DatatypeProperty))
    core.add((SEED.atime,     RDF.type, OWL.DatatypeProperty))
    core.add((SEED.size,      RDF.type, OWL.DatatypeProperty))
    core.add((SEED.uid,       RDF.type, OWL.DatatypeProperty))
    core.add((SEED.gid,       RDF.type, OWL.DatatypeProperty))

    # Bucket contain only Object
    set_property(core, (SEED.Bucket, SEED.contain, SEED.Object), only=True)

    # CompositeObject [stripe, replicate, redundancy] only SimpleObject
    set_property(core, 
        (SEED.CompositeObject, SEED.stripe,     SEED.SimpleObject), only=True)
    set_property(core, 
        (SEED.CompositeObject, SEED.replicate,  SEED.SimpleObject), only=True)
    set_property(core, 
        (SEED.CompositeObject, SEED.redundancy, SEED.SimpleObject), only=True)

    # Object name
    set_property(core,
        (SEED.Object, SEED.name, XSD.normalizedString), max_qc=1)

    # Object origin
    set_property(core,
        (SEED.Object, SEED.origin, XSD.normalizedString), max_qc=1)

    # Object stat [mode, {c|m|a}time, length, size, uid, gid]
    set_property(core, (SEED.Object, SEED.mode,  XSD.unsignedShort), max_qc=1)
    set_property(core, (SEED.Object, SEED.ctime, XSD.unsignedLong),  max_qc=1)
    set_property(core, (SEED.Object, SEED.mtime, XSD.unsignedLong),  max_qc=1)
    set_property(core, (SEED.Object, SEED.atime, XSD.unsignedLong),  max_qc=1)
    set_property(core, (SEED.Object, SEED.size,  XSD.unsignedLong),  max_qc=1)
    set_property(core, (SEED.Object, SEED.uid,   XSD.int),           max_qc=1)
    set_property(core, (SEED.Object, SEED.gid,   XSD.int),           max_qc=1)

    # Serialize the store as RDF/XML to file.
    core.serialize(DEFAULT_CORE_MODEL)

    SEED_LOG.info("produced %d triples in %s." % \
        (len(core), DEFAULT_CORE_MODEL))


def safe_stat(path):
    """run os.stat without break"""
    result = None
    try:
        result = os.stat(path)
    except Exception, stat_error:
        print 'stat error', stat_error
        result = \
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    finally:
        return result


_NODE_ID = getnode()

def read_tree(directory):
    """read directory tree, gather metadata into object_list."""
    tree = os.walk(directory)

    root_id = str(uuid1(_NODE_ID))
    root_name = os.path.basename(directory)

    object_list = \
        {
            directory:
                {
                    'id':   root_id,
                    'name': root_name,
                    'type': 'Root',
                    'contain': [],
                    'stat': safe_stat(directory)
                }
        }

    progress = 1

    for (dirpath, dirnames, filenames) in tree:

        for dirname in dirnames:
            object_id = str(uuid1(_NODE_ID))
            object_path = os.path.join(dirpath, dirname)

            object_list[object_path] = \
                {
                    'id':   object_id,
                    'name': dirname,
                    'type': 'Bucket',
                    'contain': [], # fill this later
                    'stat': safe_stat(object_path)
                }

            object_list[dirpath]['contain'].append(object_id)

            progress += 1
            if progress % 1024 is 0:
                sys.stdout.write(
                    "Traversed %d K objects\r" % int(progress >> 10))
                sys.stdout.flush()

        for filename in filenames:
            object_id = str(uuid1(_NODE_ID))
            object_path = os.path.join(dirpath, filename)

            object_list[object_path] = \
                {
                    'id':   object_id,
                    'name': filename,
                    'type': 'Object',
                    'contain': [], # files contain None
                    'stat': safe_stat(object_path)
                }

            object_list[dirpath]['contain'].append(object_id)

            progress += 1
            if progress % 1024 is 0:
                sys.stdout.write(
                    "Traversed %d K objects\r" % int(progress >> 10))
                sys.stdout.flush()

    print 'Traversed %d objects' % progress

    return object_list


XML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def xml_escape(text):
    """Produce entities within text."""
    return "".join(XML_ESCAPE_TABLE.get(c, c) for c in text)


# BEGIN: model template

T_HEADER = Template(
"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rdf:RDF [
  <!ENTITY owl "http://www.w3.org/2002/07/owl#" >
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
  <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
]>
<rdf:RDF
  xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:owl="http://www.w3.org/2002/07/owl#"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:terms="http://purl.org/dc/terms/"
  xmlns:seed="$seed_base#"
>
  <rdf:Description rdf:about="$base_uri">
    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Ontology"/>
    <owl:imports rdf:resource="$seed_base"/>
    <owl:versionInfo rdf:datatype="&xsd;hexBinary">$version</owl:versionInfo>
    <dc:created rdf:datatype="&xsd;dateTimeStamp">$created</dc:created>
    <dc:date>2013-01-31</dc:date>
    <rdfs:comment xml:lang="EN">SEED node ontology</rdfs:comment>
    <terms:license rdf:datatype="&xsd;string">$license</terms:license>
    <dc:creator>Shi.Zhan</dc:creator>
  </rdf:Description>
""")
# $seed_base, $base_uri,
# $version, $created, $license

T_INDIVIDUAL = Template(
"""
  <rdf:Description rdf:about="$base_uri#$object_id">
    <rdf:type rdf:resource="$seed_base#$object_type"/>
    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/>
    <seed:name rdf:datatype="&xsd;normalizedString">$name</seed:name>
    <seed:origin rdf:datatype="&xsd;normalizedString">$origin</seed:origin>
    <seed:mode rdf:datatype="&xsd;unsignedShort">$mode</seed:mode>
    <seed:uid rdf:datatype="&xsd;int">$uid</seed:uid>
    <seed:gid rdf:datatype="&xsd;int">$gid</seed:gid>
    <seed:size rdf:datatype="&xsd;unsignedLong">$size</seed:size>
    <seed:atime rdf:datatype="&xsd;unsignedLong">$atime</seed:atime>
    <seed:mtime rdf:datatype="&xsd;unsignedLong">$mtime</seed:mtime>
    <seed:ctime rdf:datatype="&xsd;unsignedLong">$ctime</seed:ctime>
    $contain
  </rdf:Description>
""")
# $base_uri, $seed_base, $object_id, $object_type[Bucket|Object], $name, $origin
# $mode, $uid, $gid, $size, $atime, $mtime, $ctime
# $contain

T_CONTAIN = Template("""<seed:contain rdf:resource="$base_uri#$object_id"/>
    """)
# $base_uri, $object_id

T_FOOTER = """</rdf:RDF>"""

# END: model template

def write_model(object_list, model_file):
    """write objects in list to model file"""

    base_uri = 'http://' + DEFAULT_HOST + '/' + model_file

    created = time.strftime('%Y-%m-%d %H:%M:%S',
                time.localtime(time.time())).encode('utf-8')

    model = open(model_file, 'w')

    header = T_HEADER.substitute(
                seed_base=SEED_BASE,
                base_uri=base_uri,
                version=VERSION,
                created=created,
                license=LICENSE
            )

    footer = T_FOOTER

    print >> model, header

    object_total = len(object_list)
    object_total_m1k = object_total % 1024 # update progress every 1K loop
    progress = 0

    for path, i_object in object_list.iteritems():

        # print path

        progress += 1

        if object_total > 1024 and progress % 1024 is object_total_m1k:
            sys.stdout.write(
                "Generating progress: %d%%\r" % int(100*progress/object_total))
            sys.stdout.flush()

        # build clause for object property 'contain'
        i_object_contain = ''

        if not len(i_object['contain']) == 0:
            for subobject_id in i_object['contain']:
                i_object_contain += T_CONTAIN.substitute(
                    base_uri=base_uri, object_id=subobject_id)

        # build clause for data properties, with 'contain', fill in individual
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) \
            = i_object['stat']

        i_object_text = T_INDIVIDUAL.substitute(
            base_uri=base_uri,
            seed_base=SEED_BASE,
            object_id=i_object['id'],
            object_type=i_object['type'],
            name=xml_escape(i_object['name']),
            origin=xml_escape(path),

            contain=i_object_contain,

            mode=mode,
            uid=uid,
            gid=gid,
            size=size,
            atime=atime,
            mtime=mtime,
            ctime=ctime
        )

        print >> model, i_object_text

    print '\r' # CR after flush

    print >> model, footer

    model.close()


def init_model(root_directory, model_file):
    """
    initialize models:
    1. check if core model exists (in CWD), create it if necessary;
    2. check core model version compatibility;
    3. generate node model file based on the content of root_directory.
    """
    if os.path.exists(DEFAULT_CORE_MODEL):
        SEED_LOG.info('load core model')

        core_model = Graph()
        core_model.load(DEFAULT_CORE_MODEL)

        version = core_model.value(URIRef(SEED_BASE), OWL.versionInfo)

        SEED_LOG.info('core model version: [%s]' % version)

        if not version == VERSION:
            SEED_LOG.error(
                'incompatible to program version [%s], need to regenerate.' \
                % VERSION)

            gen_core()

        else:
            SEED_LOG.info('version compatible')

    else:
        SEED_LOG.error('core model does not exist, need to generate.')

        gen_core()

    # generate node model by importing specified root directory

    root_directory = os.path.abspath(root_directory)

    if not os.path.exists(root_directory):
        SEED_LOG.error('directory not exist')
        return

    SEED_LOG.info('reading object list ...')

    object_list = read_tree(root_directory)

    SEED_LOG.info('creating node model ...')

    write_model(object_list, model_file)

    SEED_LOG.info('%d object individuals created in %s.' % \
        (len(object_list), model_file))


def create_individual(model, i_base_uri, i_type):
    """declare individual and assign type"""
    i_uri = i_base_uri + '#' + str(uuid1(_NODE_ID))
    i_node = URIRef(i_uri)

    model.add((i_node, RDF.type, OWL.NamedIndividual))
    model.add((i_node, RDF.type, i_type))

    return i_node
