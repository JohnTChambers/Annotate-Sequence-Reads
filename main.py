#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
"""
This script holds the solution to the third invitae coding task
"""
#-----------------------------------------------------------------------------
__author__ = "John chambers"
__created__ = "FEB 7 2022"
#----------------------------------------------------------------------------

import csv
import pandas as pd
import argparse

def __parse_arguments(raw_args=None):
    """
    Parse arguments when called from command line.

    :param raw_args: a list containing the raw arguments, typically provided from the command line
    :return: args.coordinates, the path to the coordinates file
    :return: args.output, the path to the output file
    :return: args.annotations, the path to the annotations file
    """
    parser = argparse.ArgumentParser(description="match chromosome and coordinates to annotation")
    parser.add_argument("coordinates", help="the path to the coordinates file")
    parser.add_argument("annotations", help="the path to the annotations file")
    parser.add_argument('-o','--output', nargs='?',type=str, help="the output file, default=./annotated_coordinates",
        default='./annotated_coordinates')
    args = parser.parse_args()
    # coordinates_file, output_file, annotations_file = args.coordinates, args.output, args.annotations
    return args.coordinates, args.output, args.annotations


def group_annotations(annotations_df):
    """
    Returns a sorted dataframe of annotations for each chromosome ready for binary searching.

    :param annotations_df: dataframe containing the annotations to be used
    :return: chromosome_dfs: a list of dataframes containing the annotations for each chromosome
    :return chromosome_series: a list of series of the end-positions for each chromosome, for binary searching
    """
    chromosome_dfs, chromosome_series = {}, {}
    for x, y in annotations_df.groupby('chr', as_index=False):
        chromosome_dfs[x] = pd.DataFrame(y)
        # concatenate the start and end coordinates of each feature, so we can perform a binary search
        start_coord = chromosome_dfs[x].drop('start', axis=1)
        end_coord = chromosome_dfs[x].drop('end', axis=1)
        coord_concat = pd.concat([start_coord, end_coord], axis=0)
        # sort the dataframe by position
        chromosome_dfs[x] = coord_concat.sort_values(by='end', axis=0, ascending=True)
        # don't forget to reset the index
        chromosome_dfs[x] = chromosome_dfs[x].reset_index(drop=True)
        # lastly, lets make it into a series for the binary search
        chromosome_series[x] = (chromosome_dfs[x])['end'].squeeze()
    return chromosome_series, chromosome_dfs



def bin_search(coordinates_file, chromosome_series, chromosome_dfs):
    """
    Perform a binary search to match sequences to their annotations, return the matched annotations.

    :param coordinates_file: file containing the coordinates to match
    :param chromosome_series: a list of series of the end-positions for each chromosome, for binary searching
    :param chromosome_dfs: a list of dataframes of the annotations for each chromosome
    :return: annotated_sequences: a dataframe containing the sequences and their annotations
    """
    print ("performing binary search to match entries with annotations...")
    # create empty outputs
    positions, chromosomes, annotations = [], [], []
    # read the coordinates
    rd = csv.reader(open(coordinates_file), delimiter="\t", quotechar='"')
    for row in rd:
        chro, position = row
        # try statement to avoid exceptions from chromosomes missing from annotations file
        try:
            # perform a binary search with pandas searchsorted method which itself is based off of numpys searchsorted
            map_left = (chromosome_series[chro]).searchsorted(int(position), side='left')
            annotation = chromosome_dfs[chro]["annotation"].loc[map_left]

            # make sure there is only one match
            # - this check can be sacrificed for speed by commenting the following two lines
            map_right = (chromosome_series[chro]).searchsorted(int(position), side='right')
            if map_left != map_right : annotation = "error - more than one match"
            # add output to list
            positions.append(position)
            chromosomes.append(chro)
            annotations.append(annotation)
        except:
            # add output to list
            positions.append(position)
            chromosomes.append(chro)
            annotations.append('chromosome not found in annotation file')
    annotated_sequences = pd.DataFrame(list(zip(chromosomes, positions, annotations)))
    return annotated_sequences

def main(coordinates_file, annotations_file, output_file):
    """

    :return:
    """
    # read and parse the annotations file
    annotations_df = pd.read_csv(annotations_file, sep='\t',
                                 names=['chr', 'refFlat', 'coding', 'start', 'end', 'score1', 'strand', 'score2',
                                        'annotation', 'z'])
    # group the annotations
    chromosome_series, chromosome_dfs = group_annotations(annotations_df)
    # perform binary search
    annotated_sequences = bin_search(coordinates_file, chromosome_series, chromosome_dfs)
    print('finishing...')
    annotated_sequences.to_csv(output_file, index=False, header=['chromosome', 'position', 'annotation'], sep='\t')
    print("finished")

if __name__ == "__main__":
    # parse args
    coordinates_file, annotations_file, output_file = __parse_arguments()
    main(coordinates_file, output_file, annotations_file)




