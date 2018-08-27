#!/usr/bin/env python

import csv

targ_genomes_file = "targ_genomes.list"

mainfilename = "/data/genome_gene_function.tsv"

targs = {}

with open( targ_genomes_file, "r") as t:
    for line in t:
        targs[ line.strip() ] = True

with open( mainfilename, "r") as f:
    rcsv = csv.reader( f, delimiter="\t" )
    for row in rcsv:
        #print( row )
        genome, gene, func = row
        #if ( genome in targs):       # positive set
        if not ( genome in targs):    # complement set
            print( func )


