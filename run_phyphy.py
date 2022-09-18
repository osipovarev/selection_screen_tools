#!/sw/bin/python3
#

import argparse
# import phyphy
try:
    import phyphy
except ImportError:
    import PHYPHY_LIB as phyphy


__author__ = "Bogdan Kirilenko, 2018."

## parse args
app = argparse.ArgumentParser(description="")
app.add_argument("-a", "--ali", type=str, help="aligned exons for a gene in fasta format")
app.add_argument("-t", "--tree", type=str, help="labeled tree in newick format")
app.add_argument("-o", "--output", type=str, default="out.tsv", help="")
app.add_argument("-m", "--method", type=str, default="relax", help="specify 'absrel' if you want to run absrel. RELAX is default")
app.add_argument("-f", "--foreground", action='store_true', help="if specified, runs aBSREL for Foreground branches; otherwise runs aBSREL on all branches")
args = app.parse_args()

method = args.method
ali_file = args.ali
tree_file = args.tree
out_file = args.output

myhyphy = phyphy.HyPhy(build_path='/projects/hillerlab/genome/src/hyphy/version2.3.11/')
if args.method == "absrel":
    if args.foreground:
        mode = "Foreground"
    else:
        mode = "All"
    myfel = phyphy.ABSREL(alignment=ali_file, tree=tree_file, output=out_file, branches=mode, hyphy=myhyphy)
else:
    myfel = phyphy.RELAX(alignment=ali_file, tree=tree_file, output=out_file, test_label="Foreground", hyphy=myhyphy)

## run the analysis
myfel.run_analysis()
