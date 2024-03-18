#!/usr/bin/env python

###############################################
#####      SCRIPT OVERVIEW: PARSE GTF     #####
###############################################
###
###     Takes in the annotation file (GTF) for reference genome and writes out a mapping file
###     that maps gene ID's to gene symbols (e.g. ENSMUSGXXXXX to Actb). THIS IS EXTREMELY
###     HARDCODED FOR GTF'S
### 
###     Input:
###         -i      Input GTF file
###
###     Output:
###         -o      Outputs a mapping file CSV that maps gene ID to gene symbol
###



#######################
####    IMPORTS    ####
#######################

import argparse
import pandas



################################## 
####     COMMAND LINE ARGS    ####
##################################

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help='The input file specified will be the GTF file provided by snakemake',dest="input", required=True) 
parser.add_argument("-o", "--output", help='The output file name and path provided by snakemake',dest="output", required=True)

args = parser.parse_args()


################################
####    GET MAPPING INFO    ####
################################
###
### Loop through GTF file and check for specifically gene regions
### Extract out gene name and gene ID information in specific columns of GTF file
###

### Read in GTF
with open(args.input, 'r') as gtf:
    gtf_lines = gtf.readlines()

### Loop over GTF
mapping_lines = []
for line in gtf_lines:
    
    # Ignore starting metadata lines
    if line.startswith('#'): 
        continue

    # Split the line by tabs into list
    split_line = line.split('\t')
    if split_line[2] == 'gene':
        gene_info = split_line[8].split()
        gene_id = gene_info[1].rstrip(';').strip('\"')
        gene_name = gene_info[5].rstrip(';').strip('\"')
        mapping = ','.join([gene_id, gene_name]) + '\n'
        mapping_lines.append(mapping)
    

### Write results into file
with open (args.output, 'w') as map_file:
    for line in mapping_lines:
        map_file.write(line)
