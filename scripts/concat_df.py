#!/usr/bin/env python

###################################
#####     SCRIPT OVERVIEW     #####
###################################
#####
##### Takes the outputs of verse for each sample and concatenates them all into one CSV
#####
##### Inputs:
#####       -i      A list of the VERSE output filenames from snakemake
#####
##### Outputs:
#####       -o      Filename for the concatenated csv output
#####



#####################
###    IMPORTS    ###
#####################

import argparse
import pandas 



###############################
###    COMMAND LINE ARGS    ###
###############################

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help='A list of the VERSE output filenames provided by snakemake', dest="input", required=True, nargs='+')
parser.add_argument("-o", "--output", help='The output file name and path provided by snakemake', dest="output", required=True)

args = parser.parse_args()

#print(args.input)
#print(args.output)



####################################
###    CONCATENATE DATAFRAMES    ### 
####################################
###
### To concatenate the files into one large dataframe, first load one of the dataframes
### with pandas and then loop over the other files to merge into the original one
###

### Set up the first dataframe to merge others into
initial_df = pandas.read_csv(args.input[0], sep='\t')
init_file_name = args.input[0].split('/')[-1]
init_sample_name = init_file_name.split('.')[0]
initial_df.rename(columns={'count': init_sample_name}, inplace=True) 


### Loop over other files to merge into first df
for i in range(1, len(args.input)):
    file_name = args.input[i].split('/')[-1]
    sample_name = file_name.split('.')[0]
    
    curr_df = pandas.read_csv(args.input[i], sep='\t')
    curr_df.rename(columns={'count': sample_name}, inplace=True)

    initial_df = pandas.merge(initial_df, curr_df, on='gene', how='left')


### Write out to csv
initial_df.to_csv(path_or_buf = args.output, index = False)
