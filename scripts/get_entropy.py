#!/usr/bin/env python

import sys
import numpy as np
import scipy.stats as stats

filename = sys.argv[1]


def get_shannon_entropy(matches: str):
    base, counts = np.unique(list(matches), return_counts=True)
    if len(base) <= 1 or np.sum(counts) <= 0:
        return 0
    return stats.entropy(counts / np.sum(counts))


with open(filename, "r") as f:
    for row in f:
        try:
            chrom, pos, matches = row.rstrip("\n").split(maxsplit=2)
            entropy = get_shannon_entropy(matches)
            if entropy <= 0:
                continue
        except:
            continue
        print(f"{chrom}\t{pos}\t{entropy}")
