seq_dict = {}
with open(snakemake.input.consensus) as f:
    for line in f:
        if line.startswith(">"):
            name = line.rstrip()[1:]
            seq_dict[name] = ""
        else:
            seq_dict[name] += line.rstrip()

with open(snakemake.input.cov) as f:
    cov = {}
    for line in f:
        ref, pos, depth = line.split()
        if not ref in cov:
            cov[ref] = {}
        depth = int(depth)
        cov[ref][int(pos)] = depth

primers = []
with open(snakemake.input.primers) as f:
    for line in f:
        if line.split()[0] == snakemake.params.reference:
            primers.append([line.split()[1], int(line.split()[2]), int(line.split()[3]), int(line.split()[4]), int(line.split()[5])])

print(primers)
with open(snakemake.input.blast) as f:
    trim_dict = {}
    for line in f:
        if line.startswith("Query="):
            name = line.rstrip()[7:]
            trim_dict[name] = {}
            for i in primers:
                trim_dict[name][i[0]] = [None, None]
        elif line.startswith("Query_"):
            q, qstart, qseq, qend = line.split()
            qline = line.rstrip()
            qstart, qend = int(qstart), int(qend)
        elif line.startswith("Subject_"):
            r, rstart, rseq, rend = line.split()
            rstart, rend = int(rstart), int(rend)
            qp = 0
            rp = 0
            qls = False
            rls = False
            rpos = None
            qpos = None
            for i in range(len(qline)):
                if qline[i] == " ":
                    if not qls:
                        qp += 1
                    qls = True
                elif qp == 2 and qline[i] != " " and qpos is None:
                    qpos = qstart
                    qls = False
                else:
                    qls = False
                if i < len(line) and line[i] == " ":
                    if not rls:
                        rp += 1
                    rls = True
                elif rpos is None and rp == 2 and line[i] != " ":
                    rpos = rstart
                    rls = False
                else:
                    rls = False
                if qp == 2 and rp == 2:
                    for j in primers:
                        if rpos == j[2]:
                            trim_dict[name][j[0]][0] = qpos
                        elif rpos == j[3]:
                            trim_dict[name][j[0]][1] = qpos - 1
                if qp == 2 and qline[i] != '-' and qline[i] != " ":
                    qpos += 1
                if rp == 2 and line[i] != '-' and line[i] != " ":
                    rpos += 1


print(trim_dict)
with open(snakemake.output.log, 'w') as o:
    o.write("Proessing {} contigs.\n\n\n".format(len(seq_dict)))
    o.write("Name\tlength\tstart\tstop\tdepth\tprimers.\n")
    deepest_depth = 0
    deepest_name = None
    for i in seq_dict:
        name, pos = i.split()
        start, stop = map(int, pos.split('-'))
        if start == 0:
            start = 1
        total_depth = 0
        length = stop - start + 1
        cov_name = "_".join(name.split("_")[:-1])
        for j in range(start, stop+1):
            total_depth += cov[cov_name][j]
        depth = total_depth/length
        overlapping_primers = []
        for j in primers:
            if len(set(range(start, stop+1)).intersection(set(range(j[1], j[4]+1)))) > 0:
                overlapping_primers.append(j[0])
        if overlapping_primers == []:
            overlapping_primers = "None"
        else:
            overlapping_primers = ','.join(overlapping_primers)
        o.write("{}\t{}\t{}\t{}\t{:.2f}\t{}\n".format(name, length, start, stop, depth, overlapping_primers))
        if depth > deepest_depth:
            deepest_depth = depth
            deepest_name = i
            deepest_primers = overlapping_primers
    seq = seq_dict[deepest_name]
    name, pos = deepest_name.split()
    start, stop = map(int, pos.split('-'))
    if deepest_name in trim_dict:
        trim_left, trim_right = trim_dict[deepest_name][deepest_primers]
    o.write("\n\n\n")
    o.write("Deepest contig: {}\n".format(deepest_name))
    o.write("Depth: {:.2f}\n".format(deepest_depth))
    o.write("Primer: {}\n".format(deepest_primers))
    o.write("Trim left: {}\n".format(trim_left))
    o.write("Trim right: {}\n".format(trim_right))

with open(snakemake.output.fasta, 'w') as o:
    o.write(">{}\n{}\n".format(name, seq[trim_left:trim_right]))
