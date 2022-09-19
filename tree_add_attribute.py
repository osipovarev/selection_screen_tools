#!/usr/bin/env python3
#
"""
Tool for marking newick-format-tree branches
"""

import argparse
import sys
import re

__author__ = "Bogdan Kirilenko, 2018. Ekaterina Oispova, 2020"


def parse_args():
    """Read args, check."""
    app = argparse.ArgumentParser()
    app.add_argument('-t', '--tree', type = str, help = 'input tree file')
    app.add_argument('-l', '--label_file', type = str, help = 'file with attributes to add to each branch in thre tree')

    if len(sys.argv) < 2:
        app.print_help()
        sys.exit(0)
    args = app.parse_args()
    return args


def read_tree(tree_file):
    ## Reads a tree file

    with open(tree_file, 'r') as inf:
        tree_content = inf.read()
    return tree_content


def get_branches(tree):
    ## Returns a list of branches

    # remove all special symbols and numbers
    filtered_str = re.sub(r'[^\w]', ' ', tree)
    filtered = [x for x in filtered_str.split() if not x.isdigit()]
    return filtered


def make_label_dict(label_file):
    ## Reads label file in format: branch \t attribute into a dictionary

    label_dict = {}
    with open(label_file, 'r') as inf:
        for line in inf.readlines():
            branch = line.rstrip().split('\t')[0]
            label = line.rstrip().split('\t')[1]
            label_dict[branch] = label
    return label_dict


def label_branches_from_dict(tree_content, branches, label_dict):
    ## Adds labels to a list of provided branches from label dictionary

    for branch in branches:
        if branch in label_dict:
            label = label_dict[branch]
        else:
            label = '1.0'

        if "_" in branch or "-" in branch:
            tree_content = tree_content.replace(branch, ':' + label)
        else:
            braced = "({}".format(branch)
            commed = ",{}".format(branch)
            tree_content = tree_content.replace(braced, "(" + branch + ':' + label)
            tree_content = tree_content.replace(commed, "," + branch + ':' + label)
    return tree_content


def main():
    ## Parse arguments
    args = parse_args()

    ## Get the entire tree from file
    tree_content = read_tree(args.tree)

    ## Remove existing labels from the tree
    remove_pattern = r':[0-9.]*'
    cleared_tree = re.sub(remove_pattern, '', tree_content)

    ## Get list of branches from the tree
    all_branches = get_branches(cleared_tree)

    ## Read file with labels for each branch
    label_dict = make_label_dict(args.label_file)

    ## Label each branch with a corresponding label; output
    labeled_tree = label_branches_from_dict(cleared_tree, all_branches, label_dict)
    sys.stdout.write(labeled_tree)


if __name__ == "__main__":
    main()
