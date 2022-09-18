#!/usr/bin/env python3
#
import argparse
from collections import defaultdict
import sys
import itertools


__author__ = "Ekaterina Osipova, 2020."


def calc_diff(f_list):
    ## Calculates difference between each pair of elements if the float list

    diff_list = []
    for pair in itertools.combinations(f_list, 2):
        diff_list.append(abs(pair[0] - pair[1]))
    return diff_list


def main():
    ## Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_alltab', type=str, help='all gene table: branch\tpval\ttrans\tgene')
    parser.add_argument('-d', '--delta', type=float, default=.01, help='min required difference in p-values; default: .01')
    parser.add_argument('-p', '--pcutoff', type=float, default=.05, help='at least one of the transcripts for a gene \
                        should have lower p-value')
    args = parser.parse_args()

    gene_branch_dict = defaultdict(list)
    ## Reads input all gene table
    with open(args.input_alltab, 'r') as inf:
        for line in inf.readlines():
            if not (line.startswith('branch')):
                branch = line.split()[0]
                pval = float(line.split()[1])
                trans = line.split()[2]
                gene = line.split()[3]
                gene_branch_dict[(gene, branch)].append((trans, pval))

    ## Output genes that are having different p-values for different transcripts
    for gene_branch in gene_branch_dict:
        transc_pval_list = gene_branch_dict[gene_branch]
        pval_list = [i[1] for i in transc_pval_list]
        if len(pval_list) > 1:
            pval_diff_list = calc_diff(pval_list)
            bool_pval_diff_list = [True if i >= args.delta else False for i in pval_diff_list]
            bool_pval_cutoff_list = [True if i <= args.pcutoff else False for i in pval_list]
            if any(bool_pval_cutoff_list) and any(bool_pval_diff_list):
                transc_pval_str = ';'.join([i[0] + ':' + str(i[1]) for i in transc_pval_list])
                print('{}\t{}\t{}'.format(gene_branch[1], transc_pval_str, gene_branch[0]))


if __name__ == "__main__":
        main()