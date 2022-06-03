import sys
import pandas as pd

exons = pd.read_csv(
    sys.argv[2],
    sep="\t",
    header=None,
    names=[
        "chr",
        "start",
        "end",
        "strand",
        "gene_id",
        "transcript_id",
        "exon_number",
    ],
)

print("chr\tpos\tgene\ttranscript\tpos_t\tdepth\tentropy")
with open(sys.argv[1], "r") as f:
    for row in f:
        contents = row.strip().split()
        chrom, pos = contents[0], int(contents[1])
        start, end = int(contents[4]), int(contents[5])
        strand = contents[6]
        gene, transcript = contents[7], contents[8]
        exon_number = int(contents[9])
        regions_of_interest = exons[
            (exons["transcript_id"] == transcript)
            & (exons["exon_number"] < exon_number)
        ][["start", "end"]]
        previous_lengths = (
            regions_of_interest["end"] - regions_of_interest["start"] + 1
        ).sum()
        if strand == "+":
            new_pos = pos - start + previous_lengths + 1
        elif strand == "-":
            new_pos = end - pos + previous_lengths + 1
        else:
            continue

        print(
            f"{chrom}\t{pos}\t{gene}\t{transcript}\t{new_pos}\t{contents[2]}\t{contents[3]}"
        )
