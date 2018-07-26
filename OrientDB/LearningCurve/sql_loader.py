#!/usr/bin/env python

import pyorient
from pprint import pprint, pformat

print "program starts."

client = pyorient.OrientDB( "localhost", 2424 )

session_id = client.connect( "*user*", "*password*" )

databases = client.db_list().__getattr__('databases')  #looks like the client's not translating to python native stuctures

pprint( databases )

client.db_open( "test_load", "*user*", "*password*" )

print "db opened."

have_genome = {}
have_function = {}

def do_sql( cmd ):
    print( cmd )
    client.command( cmd )

def create_classes():
    do_sql( "CREATE CLASS gene EXTENDS V" )
    do_sql( "CREATE CLASS genome EXTENDS V" )
    do_sql( "CREATE CLASS gene_function EXTENDS V" )
    do_sql( "CREATE CLASS resides_in EXTENDS E" )
    do_sql( "CREATE CLASS has_this_function EXTENDS E" )


def load_genome_gene_function( genome, gene, func ):

    # load genome record
    if not( genome in have_genome ):
        do_sql( "CREATE VERTEX genome SET name = '{0}'".format( genome ) )
    have_genome[genome] = True

    # load gene record
    do_sql( "CREATE VERTEX gene SET name='{0}'".format( gene ) )

    # load gene/genome connection
    do_sql( "CREATE EDGE resides_in FROM (SELECT FROM gene WHERE name = '{0}') TO (SELECT FROM genome WHERE name = '{1}')"
                 .format( gene, genome )   )

    # load function record
    if not( func in have_function ):
        do_sql( "CREATE VERTEX gene_function SET name = '{0}'".format( func ) )
    have_function[func] = True

    # load function/gene connection
    do_sql( "CREATE EDGE has_this_function FROM (SELECT FROM gene_function WHERE name = '{0}') TO (SELECT FROM gene WHERE name = '{1}')"
                 .format( func, gene )   )

input_file = "/newmount/mccorkle/ggf_1000.tsv"

create_classes()

print "loading functions <-> genes <-> genomes via sql command"

with open( input_file, "r" ) as gfile:
    for line in gfile:
        parts = line.lstrip().rstrip().split( "\t" )
        genome, gene = parts[0], parts[1]
        func = ''
        if len( parts ) > 2:
            func = parts[2]
        func = func.replace( "\\","")
        func = func.replace( "'", "\\'" )
        print( "{0} {1} [{2}]".format( genome, gene, func ) )
        load_genome_gene_function( genome, gene, func )



data = client.query( "SELECT FROM GENOME" )

pprint( data )

for d in data:
     #pprint( dir( d ) )
     print( "RID: {0}    class: {1}".format( d._rid, d._class ) )
     pprint( d._in )
     pprint( d._out )
     pprint( d.oRecordData )

data = client.query( "SELECT FROM GENE" )

pprint( data )

for d in data:
     #pprint( dir( d ) )
     print( "RID: {0}    class: {1}".format( d._rid, d._class ) )
     pprint( d._in )
     pprint( d._out )
     pprint( d.oRecordData )

print "program ends"
