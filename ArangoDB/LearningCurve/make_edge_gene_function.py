#!/usr/bin/env python

import csv

lookup = {}

with open( "/newmount/user/gene_functions.csv", "r" ) as csv_file:
    csvr = csv.reader( csv_file, delimiter=',', quotechar='"' )
    for row in csvr:
        # print( row )
        lookup[row[1]] = row[0]

print '"_from","_to"'
with open( "/newmount/user/genome_gene_function.tsv","r" ) as tab_file:
    tab = csv.reader( tab_file, delimiter='\t' )
    for row in tab:
        genome, gene, func = row
        func_key = lookup[func]
        print "\"genes/{0}\",\"gene_functions/{1}\"".format( gene, func_key )


