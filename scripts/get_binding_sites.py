#!/usr/bin/env python

import sys
import numpy as np
import scipy.stats as stats


def get_shannon_entropy(matches: str):
    base, counts = np.unique(list(matches), return_counts=True)
    if len(base) <= 1 or np.sum(counts) <= 0:
        return 0
    return stats.entropy(counts / np.sum(counts))


filename = sys.argv[1]
entropy_threshold = float(sys.argv[2])

with open(filename, "r") as f:
    for row in f:
        try:
            chrom, pos, depth, matches = row.rstrip("\n").split(maxsplit=3)
            entropy = get_shannon_entropy(matches)
            if entropy < entropy_threshold:
                continue
        except:
            continue
        print(f"{chrom}\t{pos}\t{depth}\t{entropy}")
