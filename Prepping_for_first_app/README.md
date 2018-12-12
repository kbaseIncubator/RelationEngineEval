
scripts to bootstrap the GSP query app

SupportScripts contain scripts that build ascii tables used by the basis program

pass6.py generates the p6_pairs.all similarity matrix.

  needs reactions.tsv and new_compounds.tsv (compounds.tsv with added InChI string for H+)

  pass6.py >p6_pairs.all


make_normal_modelseed_table.py

   This reads all the ModelSEED reaction tsv tables in the modelseed root directory 
    and makes a "normal" table (single records) of reaction, genome, gene.

./make_normal_modelseed_table.py >modelseed_rxn_genome_gene.tab 
