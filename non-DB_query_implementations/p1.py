#!/usr/bin/env python

import csv

filename = "/data/genome_gene_function.tsv"

with open( filename, "r") as f:
    rcsv = csv.reader( f, delimiter="\t" )
    for row in rcsv:
        #print( row )
        genome, gene, func = row
        if func == '1-propanol dehydrogenase':
            print( genome )


