#! /usr/bin//env/python

#########################################################
#####     SCRIPT OVERVIEW: FILTER COUNTS MATRIX     #####
#########################################################
###
###   Takes as input a raw counts matrix as a csv, applies a filtering metrix, 
###   and outputs the filtered counts matrix
###
###   Input:
###     -i      Input CSV that contains the conatenated counts matrix (rows are genes, columns are samples)
###
###   Output:
###     -o      Output CSV that contains original counts matrix minus rows that are all zeros (filtering metric for this project)
###



#######################
####    IMPORTS    ####
#######################

import argparse
import pandas



#################################
####    COMMAND LINE ARGS    ####
#################################

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help='The input file specified will be an unfiltered counts matrix',dest="input", required=True)
parser.add_argument("-o", "--output", help='The output file name and path provided by snakemake, a filtered counts matrix',dest="output", required=True)
args = parser.parse_args()


####################################
####    FILTER COUNTS MATRIX    ####
####################################

### Read in CSV as pandas dataframe and remove rows that are all zeroes
unfiltered_matrix = pandas.read_csv(args.input)
filtered_matrix = unfiltered_matrix.loc[(unfiltered_matrix != 0).all(axis=1), :]


### Write out csv
filtered_matrix.to_csv(path_or_buf = args.output, index = False, header=True)
