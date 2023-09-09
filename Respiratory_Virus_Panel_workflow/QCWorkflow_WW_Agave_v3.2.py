from datetime import date
import sys
import csv
import re
import string
import os.path
import fileinput
import math
import glob


today_date = date.today().strftime("%Y%m%d")
output = open(today_date + '_Respiratory_Workflow.sh', 'w')

# Folder with fastq files
fastq_files = glob.glob('./fastq/I*.fastq.gz')


name_list = []
r1_list = []
r2_list = []


for each_fastq in fastq_files:  # Obtain inumbers from sample names
    i_split = each_fastq.split('_')
    i_number = i_split[0]
    i_number = i_number.split('/')[2]
    if i_number not in name_list:
        name_list.append(i_number)
name_list.sort()

for each_i_number in name_list:  # Obtain fastq paths & filenames
    sample_fastqs = glob.glob('./fastq/' + each_i_number + '*.gz')
    sample_fastqs.sort()
    while len(sample_fastqs) > 0:
        try:
            r1_item = sample_fastqs.pop(0)
            r1_item = r1_item.rstrip('.gz')
            r1_list.append(r1_item)
            r2_item = sample_fastqs.pop(0)
            r2_item = r2_item.rstrip('.gz')
            r2_list.append(r2_item)
        except:
            print("Missing paired read for sample %s." % each_i_number)
            exit(1)


print(name_list)
print(r1_list)
print(r2_list)

# Write .sh file for fasta preparation
output.write("#!/bin/bash\n")
output.write("mkdir logFiles_2022;\n")
output.write("mkdir qc_fasta_2022;\n")
output.write("mkdir qc_fastq_2022;\n")
output.write("mkdir bowtie2_mapped_2022;\n")
output.write("mkdir counts_2022;\n")

try:
    for run, r1, r2 in zip(name_list, r1_list, r2_list):
        output.write("gunzip " + r1 + ".gz;\n")
        output.write("gunzip " + r2 + ".gz;\n")
        output.write("mkdir " + run + ";\n")
        output.write("bbduk.sh in=" + r1 + " in2=" + r2 + " ref=/mnt/storage/wastewater_analysis/respiratory_virus/workflow_files/contaminants/illumina_dna_prep_b.fa out=./" + run + "/" + run + "-adaptTrimQC_R1_2022.fastq out2=./" + run + "/" + run + "-adaptTrimQC_R2_2022.fastq k=19 hdist=1 ktrim=r qtrim=rl mink=11 trimq=30 minlength=75 minavgquality=20 removeifeitherbad=f otm=t tpe=t overwrite=t 1> ./" + run + "/" + run + "-adaptTrimQC_2022.log.txt 2>&1;\n")
        output.write("bbduk.sh in=./" + run + "/" + run + "-adaptTrimQC_R1_2022.fastq " + "in2=./" + run + "/" + run + "-adaptTrimQC_R2_2022.fastq " + "ref=/mnt/storage/wastewater_analysis/respiratory_virus/workflow_files/contaminants/phix174_ill.ref.fa.gz out=./" + run + "/" + run + "-R1-phixRemoved_2022.fastq out2=./" + run + "/" + run + "-R2-phixRemoved_2022.fastq k=31 hdist=1 overwrite=t 1> ./" + run + "/" + run + "phixRemoved_2022.log.txt 2>&1;\n")
        output.write("dedupe.sh -Xmx180g in1=./" + run + "/" + run + "-R1-phixRemoved_2022.fastq in2=./" + run + "/" + run + "-R2-phixRemoved_2022.fastq out=./" + run + "/" + run + "firstDeduplication_2022.fastq outd=./" + run + "/" + run + "firstDuplication_2022.fastq csf=dedupe.cluster.stats overwrite=t minidentity=99 1> ./" + run + "/" + run + "firstDeduplication.log_2022.txt 2>&1;\n")
        output.write("bbmerge.sh in=./" + run + "/" + run + "firstDeduplication_2022.fastq out=./" + run + "/" + run + "firstDeduplicationMerged_2022.fastq outu=./" + run + "/" + run + "firstDeduplicationUnMerged_2022.fastq 1> ./" + run + "/" + run + "firstDeduplicationMerged.log_2022.txt 2>&1;\n")
        output.write("cat ./" + run + "/" + run + "firstDeduplicationMerged_2022.fastq ./" + run + "/" + run + "firstDeduplicationUnMerged_2022.fastq > ./" + run + "/" + run + "firstDeduplicationMerged_UnMerged_2022.fastq;\n")
        output.write("dedupe.sh -Xmx180g in=./" + run + "/" + run + "firstDeduplicationMerged_UnMerged_2022.fastq out=./" + run + "/" + run + "secondDeduplication_2022.fastq outd=./" + run + "/" + run + "secondDuplication_2022.fastq csf=dedupe.cluster.stats overwrite=t minidentity=100 ac=f 1> ./" + run + "/" + run + "secondDeduplication.log_2022.txt 2>&1;\n")
        output.write("bbduk.sh in=./" + run + "/" + run + "secondDeduplication_2022.fastq out=./" + run + "/" + run + "secondDeduplication_filtered_2022.fastq minlength=75 overwrite=t 1>./" + run + "/" + run + "secondDeduplication_filtered.log_2022.txt 2>&1; \n")
        output.write("sed -n '1~4s/^@/>/p;2~4p' ./" + run + "/" + run + "secondDeduplication_filtered_2022.fastq > ./" + run + "/" + run + "secondDeduplication_filtered_2022.fasta;\n")
        output.write("bowtie2 -x /mnt/storage/wastewater_analysis/respiratory_virus/database/RVP_DB -f ./" + run + "/" + run + "secondDeduplication_filtered_2022.fasta > bowtie2_mapped_2022/" + run + "_contigsMapped.sam;\n")
        output.write("samtools view -h -F 0x900 bowtie2_mapped_2022/" + run + "_contigsMapped.sam > bowtie2_mapped_2022/" + run + "_secondaryRemoved.sam;\n")
        output.write("samtools view -h -F 0x4 bowtie2_mapped_2022/" + run + "_secondaryRemoved.sam > bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved.sam;\n")
        output.write("samtools view -S -b bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved.sam > bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved.bam;\n")
        output.write("samtools sort bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved.bam > bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved_sorted.bam;\n")
        output.write("samtools index bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved_sorted.bam;\n")
        output.write("samtools idxstats bowtie2_mapped_2022/" + run + "_secondaryUnMappedRemoved_sorted.bam > bowtie2_mapped_2022/" + run + ".txt\n")
        output.write("cp ./" + run + "/" + run + "-adaptTrimQC_2022.log.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "phixRemoved_2022.log.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "hostRemoval.log_2022.txt ./logFiles_2022;\n")  # ? Is there a missing step re: human genome removal?
        output.write("cp ./" + run + "/" + run + "firstDeduplication.log_2022.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "firstDeduplicationMerged.log_2022.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "secondDeduplication.log_2022.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "secondDeduplication_filtered.log_2022.txt ./logFiles_2022;\n")
        output.write("cp ./" + run + "/" + run + "secondDeduplication_filtered_2022.fastq ./qc_fastq_2022;\n")
        output.write("cp ./" + run + "/" + run + "secondDeduplication_filtered_2022.fasta ./qc_fasta_2022;\n")
        output.write("mv ./bowtie2_mapped_2022/" + run + ".txt ./counts_2022;\n")
except (ValueError, NameError) as error_message:
    print("The following error occurred: " + str(error_message))
    sys.exit(1)
