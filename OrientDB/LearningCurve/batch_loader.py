#!/usr/bin/env python

import pyorient
from pprint import pprint, pformat


functions_file = "functions_count"
genomes_file = "/newmount/mccorkle/genome_count.tab"
feature_file = "/newmount/mccorkle/ggf_1000.tsv"

sql_cmd_buffer_size = 100

total_gene_count = 0

print "program starts."

client = pyorient.OrientDB( "localhost", 2424 )

session_id = client.connect( "user", "password" )

client.db_open( "test_load", "user", "password" )

print "db opened."

def do_immediate_sql( cmd, expect_res = True ):
    # print( cmd )
    res = client.command( cmd )
    if expect_res:
        return ( [ r._rid for r in res] );
    else:
        return

sql_cmd_count = 0
sql_cmd_total = 0

sql_cmd_queue = "begin;\n"
sql_flush = True

def set_flush( v ):
    global sql_flush
    sql_flush = v

def flush_sql_cmd_queue():
    global sql_cmd_queue
    global sql_cmd_count
    global sql_cmd_total
    global sql_flush
    if sql_flush and sql_cmd_count >= sql_cmd_buffer_size:
        if sql_cmd_count > 0:
            sql_cmd_total = sql_cmd_total + sql_cmd_count
            sql_cmd_queue = sql_cmd_queue + "commit retry 100"
            client.batch( sql_cmd_queue )
        sql_cmd_count = 0
        sql_cmd_queue = "begin;\n"

def do_batch_sql( cmd ):
    global sql_cmd_queue
    global sql_cmd_count
    sql_cmd_queue = sql_cmd_queue + cmd + ";\n"
    sql_cmd_count = sql_cmd_count + 1
    flush_sql_cmd_queue()

def load_genome_gene_function( genome, gene, func ):

    set_flush( False )    # suppress flushing() for this cluster of commands

    # load gene record
    do_batch_sql( "let g_rid = CREATE VERTEX gene SET name='{0}'".format( gene ) )

    # load gene/genome connection
    do_batch_sql( "CREATE EDGE resides_in FROM $g_rid TO {0}".format( genome_rid[genome] ) )

    # load function/gene connection 
    if func != '':
        do_batch_sql( "CREATE EDGE has_this_function FROM {0} TO $g_rid".format( function_rid[func] )  )

    set_flush( True )
    flush_sql_cmd_queue()

def create_tables():
    do_immediate_sql( "CREATE CLASS gene EXTENDS V", expect_res = False )
    do_immediate_sql( "CREATE CLASS genome EXTENDS V", expect_res = False )
    do_immediate_sql( "CREATE CLASS gene_function EXTENDS V", expect_res = False )
    do_immediate_sql( "CREATE CLASS resides_in EXTENDS E", expect_res = False )
    do_immediate_sql( "CREATE CLASS has_this_function EXTENDS E", expect_res = False )

# creating tables

create_tables()

# create function_rid table

print "doing functions..."

function_rid = {}
with open( functions_file, "r" ) as ffile:
    for line in ffile:
        parts = line.lstrip().rstrip().split( " ", 1 )
        #print( parts )
        if  len( parts ) > 1:
            func = parts[1]
            func = func.replace( "\\","")
            func = func.replace( "'", "\\'" )
            rid = do_immediate_sql( "CREATE VERTEX gene_function SET name = '{0}'".format( func ) )[0]
            function_rid[ func ] = rid

#for func in function_rid.keys():
#    print( func )

# create genome_rid table
print "doing genomes ..."

genome_rid = {}
with open( genomes_file, "r" ) as gfile:
    for line in gfile:
        parts = line.lstrip().rstrip().split( " " )
        #print( parts )
        if  len( parts ) > 1:
            genome = parts[1]
            rid = do_immediate_sql( "CREATE VERTEX genome SET name = '{0}'".format( genome ) )[0]
            #print "{0}: {1}".format( genome, rid )
            genome_rid[ genome ] = rid

# laad genes and links

print "loading functions <-> genes <-> genomes via sql command"

with open( feature_file, "r" ) as ffile:
    for line in ffile:
        parts = line.lstrip().rstrip().split( "\t" )
        genome, gene = parts[0], parts[1]
        total_gene_count = total_gene_count + 1
        func = ''
        if len( parts ) > 2:
            func = parts[2]
        func = func.replace( "\\","")
        func = func.replace( "'", "\\'" )
        #print( "{0} {1} [{2}]".format( genome, gene, func ) )
        load_genome_gene_function( genome, gene, func )
    flush_sql_cmd_queue()


print "program ends."
