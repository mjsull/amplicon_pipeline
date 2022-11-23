# PRIMER Analysis

SSH into Disco

Create a new folder with the directory name
$ cd /data/MPX
$ mkdir <directory name - YYMMDDMPX>

Activate conda environment
$ conda activate mpx

For each sample do the following:
PRIMER runs
Run snakemake, check the barcode that the lab is using on the samplesheet.
$ snakemake --snakefile /data/MPX/mpx_primer/SnakeMake trim_consensus --config workdir=/data/MPX/<directory>/barcodeXX ont_folder=<dir-on-nanopore> barcode=<barcode_number>  --cores 32 --use-conda

example:
$ snakemake --snakefile ~/mpx_primer/SnakeMake trim_consensus --config workdir=/data/MPX/220811MPX/barcode67 ont_folder=/mnt/phm/gridion2/MPX220809/G2_X4/20220809_1710_X4_FAU11736_a08a2df2/ barcode=barcode67  --cores 32 --use-conda

Review ouput
Look at log barcodeXX/data/log.txt.
   - Scroll to end of file
   - Look at the the selected primer, check that the correct primers have been amplified (mpx for XXXXXXXX-MPX samples and ortho for XXXXXXX-ORTHO samples).
   - Look at the depth, is it good (and much higher than the off target consensus sequences)
   - Look at the trimming, have both sides been trimmed?


Once the pipeline has been run for each barcode concatenate the cosensus (barcodeXX/data/consensus.trimmed.fasta) to <sample>_MX<NNNNN>.fasta) where sample is the sample ID and <NNNNN> is the sequence ID. i.e. (cat barcode01/data/consensus.trimmed.fasta barcode02/data/consensus.trimmed.fasta > S83744_MX00005.fasta). Copy the files to   
G:\PEH Genomics\Reports\MPXV\YYYYMMDD
Rename the fasta headers to MXNNNNN_ortho for the orthopox primers and MXNNNNN_mpx for the mpx specific primers. If one sample has more than one sequencing run double check that the sequences are identical and remove duplicates.


Email Alyssa with directory to complete report.

# Metagenomics analysis

SSH into Disco

Create a new folder with the directory name
$ cd /data/MPX
$ mkdir <directory name - YYMMDDMPX>

Activate conda environment
$ conda activate mpx

For each sample do the following:

Run snakemake, check the barcode that the lab is using on the samplesheet.
$ snakemake --snakefile /data/MPX/mpx_primer/SnakeMake consensus --config workdir=/data/MPX/<directory>/<sample>-MPX illumina_read_1=</path/to/read1.fastq.gz> illumina_read_2=</path/to/read2.fastq.gz>  --cores 32 --use-conda

example:
$ snakemake --snakefile ~/mpx_primer/SnakeMake consensus --config workdir=/data/MPX/220811MPX/SS22S77952-MPX illumina_read_1=/path/to/read1.fastq.gz illumina_read_2=/path/to/read2.fastq.gz  --cores 32 --use-conda

Review ouput:
Load bam file (/data/MPX/<YYYYMMDD>MPX/<sample>-MPX/data/aligned.sorted.bam in viewer, make sure there are no gaps and whole genome is covered.

Once the pipeline has been run for each barcode copy the cosensus (/data/MPX/<YYYYMMDD>MPX/<sample>-MPX/data/consensus.fasta) to <sample>_MX<NNNNN>.fasta) where sample is the sample ID and <NNNNN> is the sequence ID. i.e. (cp /data/MPX/220831MPX/SS22S77952-MPX/data/consensus.fasta > S83744_MX00005.fasta). Copy the files to   
G:\PEH Genomics\Reports\MPXV\YYYYMMDD

Rename the fasta headers to MXNNNNN_meta.


Email Alyssa with directory to complete report.