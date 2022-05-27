#!/bin/bash

samtools mpileup binfo1-datapack1/RNA-control.bam > RNA-control.pileup
samtools mpileup binfo1-datapack1/CLIP-35L33G.bam | tee CLIP-35L33G.pileup | \
awk '{if ($4 > 10) {print $1,$2,$5}}' | sed 's/[!<>$*#^&]//g' > pileup_simplified.tsv
cat binfo1-datapack1/gencode.gtf | awk '{OFS="\t"}{if ($3 == "exon") {print $1,$4,$5,$7,$10}}' > exons.bed

scripts/get_entropy.py pileup_simplified.tsv | awk '{OFS="\t"}{print $1,$2,$2+1,$3}' > entropy.tsv
bedtools intersect \
-a <(cat binfo1-datapack1/gencode.gtf | awk '{OFS="\t"}{if ($3 == "exon") {print $1,$4,$5,$7,$10,$24}}') \
-b <(cat entropy.tsv | awk '{OFS="\t"}{print $1}') -wa -wb | cut -f 4,5- | awk '{OFS="\t"}{print $2,$3,$4,$5,$6,$1,$7}' > candidate_binding_sites.tsv
python scripts/get_binding_sites.py candidate_binding_sites.tsv > binding_sites.tsv
python scripts/get_flanking_sequence.py binding_sites.tsv binfo1-datapack1/genome.fa.gz > binding_sites_flanking_sequence.tsv

