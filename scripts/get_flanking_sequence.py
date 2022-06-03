import sys
import subprocess
import argparse
import pandas as pd
from tqdm import tqdm


def get_reverse_complement(sequence):
    new_sequence = ""
    for base in sequence[::-1]:
        try:
            new_sequence += REVERSE_COMPLEMENT[base]
        except:
            new_sequence += "N"

    return new_sequence


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-s", "--sequence", required=True)
parser.add_argument("-f", "--feature", default="chr")
parser.add_argument("-v", "--value", default="pos")
args = parser.parse_args()

binding_sites = []
common_command = ["samtools", "faidx", args.sequence]

flanking_seqence_data = []
print(
    "\t".join(
        [
            "chr",
            "pos",
            "gene",
            "transcript",
            "pos_t",
            "depth",
            "entropy",
            "sequence",
        ]
    )
)
for data in pd.read_csv(args.input, sep="\t", chunksize=1000):
    left_bound = data[args.value] - 10
    left_bound[left_bound < 1] = 1
    right_bound = data[args.value] + 10
    data["coordinate"] = (
        data[args.feature]
        + ":"
        + left_bound.astype("str")
        + "-"
        + right_bound.astype("str")
    )
    cmd = common_command + data["coordinate"].to_list()
    data.set_index("coordinate", inplace=True, drop=False)
    sequences = {}
    current_name = None
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        for row in proc.stdout:
            content = row.decode()
            if content.startswith(">"):
                current_name = content.strip(">").strip()
                sequences[current_name] = ""
                continue
            sequences[current_name] += content.strip()
    print(
        data.join(pd.Series(sequences, name="sequence"))[
            [
                "chr",
                "pos",
                "gene",
                "transcript",
                "pos_t",
                "depth",
                "entropy",
                "sequence",
            ]
        ]
        .dropna()
        .to_csv(sep="\t", index=False, header=False)
    )
    flanking_seqence_data.append(data.dropna())


# print(
#     pd.concat(flanking_seqence_data, axis=0, ignore_index=True).to_csv(
#         sep="\t", index=False, header=True
#     )
# )
