import sys
import pandas as pd

binding_sites = []

for data in pd.read_csv(
    sys.argv[1],
    sep="\t",
    header=None,
    usecols=[0, 1, 2, 3, 5, 6],
    names=["gene", "exon", "chr", "pos", "strand", "entropy"],
    chunksize=100000,
):
    data[["gene", "exon"]] = data[["gene", "exon"]].apply(
        lambda x: x.str.strip(";")
    )
    data = data[data["entropy"] > 0.8]
    binding_sites.append(data)

binding_sites = pd.concat(binding_sites, axis=0, ignore_index=True)
print(binding_sites.to_csv(sep="\t", index=False, header=True))
