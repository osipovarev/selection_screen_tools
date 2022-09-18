#!/usr/bin/env python3
#
import argparse
import json


__author__ = "Ekaterina Osipova, 2020."


def main():
    ## Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jsonmeme', type=str, help='file with json output of MEME')
    parser.add_argument('-a', '--attribute', type=str, default='p-value', help='attribute of MLE-content you want to extract; \
                        ltr/p-value/nbranches/lbranch; default: p-value')
    args = parser.parse_args()

    ## Read MEME output into json object
    with open(args.jsonmeme, 'r') as inf:
        data = json.load(inf)

    ## Get requested attribute
    attribute = args.attribute
    content = data['MLE']['content']['0']
    if attribute == 'ltr':
        index = 5
    elif attribute == 'p-value':
        index = 6
    elif attribute == 'nbranches':
        index = 7
    elif attribute == 'lbranch':
        index = 8

    ## Output requested attribute for each site
    i = 1
    for site in content:
        print('{}\t{}'.format(i, site[index]))
        i += 1

if __name__ == "__main__":
    main()
