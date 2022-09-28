#!/usr/bin/env python3
#
'''
This script estimates the date of a gene loss on a selected branch,
based on the divergence times of the ancestor and descendant.
'''
import argparse
import subprocess
import re
import sys


__author__ = "Ekaterina Osipova, 2022."


def pseudo_branch_estimate(ta, td, wf, wb, s):
    ## Makes an estimate of a loss based on the time estimates for the branch and omega values

    l_mixed = ta - td
    l_func = l_mixed * (1 - wf) / (1 - wb)
    l_pseudo = l_mixed - l_func
    corr_l_func = l_mixed / (1 + l_pseudo / l_func * s)
    corr_l_pseudo = l_mixed - corr_l_func
    return corr_l_pseudo


def run_relax(ali, tree):
    ## Run RELAX to estimate omega values for Foreground and Background branches

    relax_command = 'hyphy relax -a {} -t {} --branches Foreground'.format(ali, tree)
    print('Running RELAX now: \n {}'.format(relax_command))
    subprocess.run(relax_command.split())


def run_codeml(ctl):
    ## Run codeml to estimate omega values for Foreground and Background branches

    codeml_command = 'codeml {}'.format(ctl)
    print('Running codeml now: \n {}'.format(codeml_command))
    subprocess.run(codeml_command.split())


def parse_codeml_out(ctl):
    ## Parse codeml output .mlc file specified in .ctl file to get omega values

    grep_mlc_command = 'grep outfile {}'.format(ctl)
    grep_mlc = subprocess.Popen(grep_mlc_command.split(), stdout=subprocess.PIPE)
    mlc_line = grep_mlc.stdout.read()
    mlc_file = mlc_line.decode().split('=')[1].split()[0]

    with open(mlc_file, 'r') as inf:
        for line in inf.readlines():
            if re.search("\(dN/dS\)", line):
                print(line)
                omega_values = line.split(':')[-1].split()
                omega_bg = float(omega_values[0])
                omega_fg = float(omega_values[-1])
                return omega_fg, omega_bg


def main():
    ## Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-ta',
        '--tancestor',
        type=float,
        help='T estimate of the ancestral divergence, MYA'
    )
    parser.add_argument(
        '-td',
        '--tdescendant',
        type=float,
        help='T estimate of the descendant divergence, MYA'
    )
    parser.add_argument(
        '-wf',
        '--omegafg',
        type=float,
        help='provide omega (w) estimate for the loss branch (foreground) if you have it'
    )
    parser.add_argument(
        '-wb',
        '--omegabg',
        type=float,
        help='provide omega (w) estimate for the background branches if you have it'
    )
    parser.add_argument(
        '-upta',
        '--uptancestor',
        type=float,
        help='upper T estimate of the ancestral divergence, MYA'
    )
    parser.add_argument(
        '-lowta',
        '--lowtancestor',
        type=float,
        help='lower T estimate of the ancestral divergence, MYA'
    )
    parser.add_argument(
        '-uptd',
        '--uptdescendant',
        type=float,
        help='upper T estimate of the descendant divergence, MYA'
    )
    parser.add_argument(
        '-lowtd',
        '--lowtdescendant',
        type=float,
        help='lower T estimate of the descendant divergence, MYA'
    )
    parser.add_argument(
        '-s',
        '--dsratio',
        type=float,
        default=0.7,
        help='ratio dS of a functional gene is 0.7 to dS of an inactivated gene; default = 0.7'
    )
    parser.add_argument(
        '-c',
        '--ctl',
        type=str,
        help='ctl file to run codeml => to estimate omega (w) values'
    )
    parser.add_argument(
        '-t',
        '--tree',
        type=str,
        help='tree file to run RELAX => to estimate omega (w) values'
    )
    parser.add_argument(
        '-a',
        '--ali',
        type=str,
        help='codon alignment file for the gene to run RELAX => to estimate omega (w) values'
    )

    args = parser.parse_args()

    ## Required arguments
    ta = args.tancestor
    td = args.tdescendant
    ## Preferred arguments
    wf = args.omegafg
    wb = args.omegabg
    ## Optional arguments
    upta = args.uptancestor
    uptd = args.uptdescendant
    lowta = args.lowtancestor
    lowtd = args.lowtdescendant
    bound_estimates = set([upta, uptd, lowta, lowtd])
    s = args.dsratio
    ## For omega estimation
    ali = args.ali
    tree = args.tree
    ctl = args.ctl

    ## Check required arguments
    if ta == None or td == None:
        print('T ancestral or T descendant are not provided! exit')
        sys.exit(1)

    ## Estimate omega (w) values with codeml/RELAX
    if wf == None or wb == None:
        print('omega estimates for Foreground or Background branches were not provided . . .\n \
         Running codeml to estimate omega values')

        if ctl == None:
            print('.ctl file to run codeml is not provided! exit')
            exit(1)
        else:
            run_codeml(ctl)
            wf, wb = parse_codeml_out(ctl)
            print('Estimated omega Foreground: {}; Background: {}'.format(wf, wb))


    ## Make point estimate the loss date
    corr_l_pseudo = pseudo_branch_estimate(ta, td, wf, wb, s)
    tloss = td + corr_l_pseudo
    print("the gene was lost: {} MYA".format(tloss))

    ## Make upper and lower estimates if arguments are provided
    if None in bound_estimates:
        if bound_estimates != {None}:
            print('You did not provide enough T estimates for upper and lower bounds!')
            sys.exit(1)
    else:
        ## Make upper estimate
        up_corr_l_pseudo = pseudo_branch_estimate(upta, lowtd, wf, wb, s)
        up_tloss = uptd + up_corr_l_pseudo

        ## Make lower estimate
        low_corr_l_pseudo = pseudo_branch_estimate(lowta, uptd, wf, wb, s)
        low_tloss = lowtd + low_corr_l_pseudo

        ## Output estimates
        print("the upper estimate: {} MYA".format(up_tloss))
        print("the lower estimate: {} MYA".format(low_tloss))




if __name__ == "__main__":
    main()
