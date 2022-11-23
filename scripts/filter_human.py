import gzip

filter_set = set()
with open(snakemake.input.human_paf) as f:
    for line in f:
        qname, qlen, qstart, qstop, strand, rname, rlen, rstart, rstop, matches, length, mapq = line.split()[:12]
        qlen, matches, length = float(qlen), float(matches), float(length)
        if length > qlen * 0.75 and matches/length > 0.9:
            filter_set.add(qname)


print("Filtering {} reads.".format(len(filter_set)))

with gzip.open(snakemake.input.read1, 'rt') as f, gzip.open(snakemake.output.read1, 'wt') as o:
    while True:
        l1 = f.readline()
        l2 = f.readline()
        l3 = f.readline()
        l4 = f.readline()
        if l1 == "":
            break
        elif not l1.split()[0][1:] in filter_set:
            o.write(l1 + l2 + l3 + l4)


with gzip.open(snakemake.input.read2, 'rt') as f, gzip.open(snakemake.output.read2, 'wt') as o:
    while True:
        l1 = f.readline()
        l2 = f.readline()
        l3 = f.readline()
        l4 = f.readline()
        if l1 == "":
            break
        elif not l1.split()[0][1:] in filter_set:
            o.write(l1 + l2 + l3 + l4)