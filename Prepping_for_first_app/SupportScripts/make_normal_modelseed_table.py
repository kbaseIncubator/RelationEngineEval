#!/usr/bin/env python

# This reads all the ModelSEED reaction tsv tables in the modelseed root directory 
# and makes a "normal" table (single records) of reaction, genome, gene.
# This does not pay attention to the logic formulation of complexes.  Any gene
# which appears in the formula is counted.
# Unknown genes are removed.
# This also doesn't bother removing duplicates
# Resultant table is unsorted.  Records are in order of appearance in the directory
# scan.

import glob
import os.path
import re

ms_root_dir = "/newmount/mccorkle/model_objects/"

files = glob.glob( ms_root_dir + "*.mdl-reactions.tsv" )

for file in files:
    genome =  os.path.basename( file )
    genome = re.sub( '\.mdl-reactions.tsv$', '', genome )
    with open( file ) as f:
        next( f )   # skip header
        for line in f:
            parts = line.strip().split( "\t" )
            if len( parts ) > 10:
                rxn, complex = ( parts[10], parts[3] )
                complex = complex.replace( 'and', '' ).replace( 'or', '' ).replace('(','').replace( ')', '' ).lstrip().rstrip()
                genes = complex.split()
                for gene in genes:
                    if gene != "Unknown":
                        print( "{0} {1} {2}".format( rxn, genome, gene ) )


