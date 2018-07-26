#!/usr/bin/env python

import pyorient
from pprint import pprint, pformat

print "program starts."

client = pyorient.OrientDB( "localhost", 2424 )

session_id = client.connect( "user", "password" )

databases = client.db_list().__getattr__('databases')  #looks like the client's not translating to python native stuctures

pprint( databases )

client.db_open( "test_load", "user", "password" )

print "db opened."

genome_rid = {}
function_rid = {}

def do_sql( cmd ):
    print( cmd )
    res = client.command( cmd )
    return res

def create_tables():
    do_sql( "CREATE CLASS gene EXTENDS V" )
    do_sql( "CREATE CLASS genome EXTENDS V" )
    do_sql( "CREATE CLASS gene_function EXTENDS V" )
    do_sql( "CREATE CLASS resides_in EXTENDS E" )
    do_sql( "CREATE CLASS has_this_function EXTENDS E" )


def load_genome_gene_function( genome, gene, func ):

    # load genome record
    if not( genome in genome_rid ):
        res = do_sql( "CREATE VERTEX genome SET name = '{0}'".format( genome ) )
        genome_rid[genome] = res[0]._rid

    # load gene record
    res = do_sql( "CREATE VERTEX gene SET name='{0}'".format( gene ) )
    gene_rid = res[0]._rid

    # load gene/genome connection
    do_sql( "CREATE EDGE resides_in FROM {0} TO {1}".format( gene_rid, genome_rid[genome] ) )

    # load function record
    if not( func in function_rid ):
        res = do_sql( "CREATE VERTEX gene_function SET name = '{0}'".format( func ) )
        function_rid[func] = res[0]._rid

    # load function/gene connection
    do_sql( "CREATE EDGE has_this_function FROM {0} TO {1}".format( function_rid[func], gene_rid )  )

input_file = "/newmount/mccorkle/ggf_1000.tsv"

#create_tables()

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
