#!/usr/bin/env bash
#

iso_file=$1
absrel_dir=$2
suff=$3
pref=$4

if [ -z $pref ];
then
	pref=''
fi


while IFS= read -r line
do
	gene=$(echo $line | cut -d' ' -f1)
	trans=$(echo $line | cut -d' ' -f2)
#	echo -e "file im looking for: $absrel_dir/$gene/$trans/$pref.$trans.$suff"
	if [ -s "$absrel_dir/$gene/$trans/$pref.$trans.$suff"  ]; then
#		echo -e 'Running: sed "s/$/\t$trans\t$gene/" "$absrel_dir/$gene/$trans/$pref.$trans.$suff"' 
		sed "s/$/\t$trans\t$gene/" "$absrel_dir/$gene/$trans/$pref.$trans.$suff"
	fi
done < $iso_file
