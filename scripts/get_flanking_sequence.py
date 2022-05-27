import sys
import subprocess
import pandas as pd
from tqdm import tqdm

binding_sites = []
common_command = ["samtools", "faidx", sys.argv[2]]
REVERSE_COMPLEMENT = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G",
    "R": "Y",
    "Y": "R",
    "N": "N",
}


def get_reverse_complement(sequence):
    new_sequence = ""
    for base in sequence[::-1]:
        try:
            new_sequence += REVERSE_COMPLEMENT[base]
        except:
            new_sequence += "N"

    return new_sequence


flanking_seqence_data = []
for data in pd.read_csv(
    sys.argv[1],
    sep="\t",
    chunksize=1000,
):

    cmd = (
        common_command
        + (
            data["chr"]
            + ":"
            + (data["pos"] - 10).astype("str")
            + "-"
            + (data["pos"] + 10).astype("str")
        ).to_list()
    )
    sequences = []
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        for row in proc.stdout:
            if row.decode().startswith(">"):
                continue
            sequences.append(row.decode().strip())
    data["sequence"] = sequences
    data.loc[data["strand"] == "-", "sequence"] = data["sequence"].apply(
        get_reverse_complement
    )
    flanking_seqence_data.append(data)


print(
    pd.concat(flanking_seqence_data, axis=0, ignore_index=True).to_csv(
        sep="\t", index=False, header=True
    )
)
