configfile: workflow.source_path("config.yaml")
workdir: config["workdir"]


onsuccess:
    print("Workflow finished, no error")

onerror:
    print("An error occurred")

rule copy_files:
    params:
        reference = workflow.source_path("data/{}.reference.fasta".format(config["reference"])),
        primers = workflow.source_path("data/primer_pos.tsv"),
    output:
        reference = "data/reference.fasta",
        primers = "data/primers.tsv"
    shell:
        "cp {params.reference} {output.reference} && "
        "cp {params.primers} {output.primers}"


rule cat_reads:
    params:
        ont_folder = config["ont_folder"],
        barcode = config["barcode"]
    output:
        reads = "data/reads.fastq.gz"
    shell:
        "cat {params.ont_folder}/fastq_pass/{params.barcode}/*.fastq.gz > {output.reads}"




rule consensus_call:
    input:
        reference = "data/reference.fasta",
        reads = "data/reads.fastq.gz"
    output:
        consensus = "data/medaka/consensus.fasta",
        bam = "data/medaka/calls_to_draft.bam"
    shell:
        "medaka_consensus -i {input.reads} -d {input.reference} -o data/medaka -g"


rule blast_consensus:
    input:
        reference = "data/reference.fasta",
        consensus = "data/medaka/consensus.fasta"
    output:
        blast = "data/blast.out"
    shell:
        "blastn -query {input.consensus} -subject {input.reference} -outfmt 4 -out {output.blast}"

rule get_depth:
    input:
        bam = "data/medaka/calls_to_draft.bam"
    output:
        cov = "data/depth.tsv"
    shell:
        "samtools depth -aa {input.bam} > {output.cov}"
    



rule trim_consensus:
    input:
        consensus = "data/medaka/consensus.fasta",
        cov = "data/depth.tsv",
        blast = "data/blast.out",
        primers = "data/primers.tsv"
    params:
        reference = config["reference"]
    output:
        fasta = "data/consensus.trimmed.fasta",
        log = "data/log.txt"
    script:
        "scripts/trim_consensus.py"
