#!/bin/bash
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M29/gencode.vM29.transcripts.fa.gz
samtools mpileup binfo1-datapack1/CLIP-35L33G.bam  | \
awk '{if ($4 > 10) {print $1,$2,$5}}' | sed 's/[!<>$*#^&]//g' > pileup_simplified.tsv
cat binfo1-datapack1/gencode.gtf | awk '{OFS="\t"}{if ($3 == "exon") {print $1,$4,$5,$7,$10,$12,$22}}' | sed 's/"//g' | sed 's/;//g' > exons.bed

scripts/get_binding_sites.py pileup_simplified.tsv 0.8 > binding_sites.tsv
bedtools intersect -a <(cat binding_sites.tsv | awk '{OFS="\t"}{print $1,$2,$2+1,$3,$4}') \
-b exons.bed -wa -wb | cut -f 1,2,4,5,7,8,9,10,11,12 > binding_sites_with_exons.tsv
python scripts/convert_to_transcriptome_coordinate.py binding_sites_with_exons.tsv exons.bed > binding_sites_transcriptome.tsv
python scripts/get_flanking_sequence.py binding_sites_transcriptome.tsv binfo1-datapack1/transcriptome.fa.gz > binding_sites_flanking_sequence.tsv
