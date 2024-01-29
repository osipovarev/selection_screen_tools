#!/usr/bin/env bash
#

gene_file=$1
msa_final_dir=$2
absrel_dir=$3
# only these transcripts are to be considered
qual_trans=$4
# suffix to remove
suff=$5

for gene in $(cut -f1 $gene_file);
do
	if [ -d $msa_final_dir/$gene/  ]; then

		for t in $(ls $msa_final_dir/$gene/)
		do
			if  grep -q "${t%$suff}" $qual_trans ; then
				ans_tree=${t%$suff}.ans.tree
				out_file="out_v58_srv.${t%$suff}.json"
				log="out_v58_srv.${t%$suff}.log"
				echo "hyphy absrel --srv Yes --alignment $msa_final_dir/$gene/$t --tree $absrel_dir/$gene/${t%$suff}/${t%$suff}.ans.tree --output $absrel_dir/$gene/${t%$suff}/$out_file &> $log"
			fi
		done
	fi
done

