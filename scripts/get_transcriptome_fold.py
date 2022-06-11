import sys
import gzip
import pandas as pd
from get_sequence_fold import get_dot_bracket
from Bio import SeqIO

print("transcript\tsequence\tfold")
with gzip.open(sys.argv[1], "rt") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        transcript = record.id
        print(transcript)
        sequence = record.seq
        print(sequence)
        fold = get_dot_bracket(sequence)
        print(f"{transcript}\t{sequence}\t{fold}")