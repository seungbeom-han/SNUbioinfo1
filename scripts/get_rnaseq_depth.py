import sys
import subprocess

binding_sites = pd.read_csv(sys.argv[2], sep="\t").iterrows()

print(
    "chr\tpos\tgene\ttranscript\tpos_t\tdepth\tentropy\tchr_ctrl\tpos_ctrl\tdepth_ctrl"
)

with subprocess.Popen(f"samtools mpileup {sys.argv[1]}", shell=True) as proc:
    for row in proc.stdout:
        chrom, pos, _, depth, _ = row.decode().strip().split(maxsplit=4)
        _, binding_site = binding_sites.next()
        while binding_site["chr"] != chrom and binding_site["pos"] < int(pos):
            prev_depth = binding_site["depth"]
            _, binding_site = binding_sites.next()
        print("\t".join(binding_site.to_list() + [chrom, pos, depth]))
