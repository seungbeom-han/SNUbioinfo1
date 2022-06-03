from tqdm import tqdm
import subprocess
import pandas as pd

fold_sequence = lambda x: subprocess.run(["seqfold", "-d", x], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")[1]

binding_sites = pd.read_csv("binding_sites_flanking_sequence.tsv", sep="\t")
sequences = pd.Series(index=binding_sites.sequence.unique())
for sequence in sequences.index.to_series():
    sequences[sequence] = fold_sequence(sequence)
print(binding_sites.set_index("sequence").join(sequences).to_csv("binding_sites_fold.tsv", sep="\t", index=False))