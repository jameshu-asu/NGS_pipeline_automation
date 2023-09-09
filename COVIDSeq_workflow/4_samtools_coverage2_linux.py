from run import run
import subprocess
import csv
import pandas as pd
import os
import fnmatch

'''By James C. Hu
This script will:
1) Generate coverage outputs for all bam files within a directory.
2) Compile coverage data into a single output.
'''

os.chdir(f'../NextSeq1000_{run}_Analysis/bam_files')
subprocess.run('ls *.bam > bam_list.txt', shell=True)

bam_list = []

with open("bam_list.txt", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[0])
        bam_list.append(row[0])

for each in bam_list:
    current_out_file = str(str(each) + ".txt")
    subprocess.run(f'samtools coverage {each} -o  {each}.txt', shell=True)

subprocess.run("mv *.bam.txt ../coverage_files/", shell=True)
subprocess.run('mv bam_list.txt ../freyja_output_processing/', shell=True)

os.chdir('../coverage_files/')

coverage_list = []
coverage_list = os.listdir()

filtered_coverage_list = []

for file in os.listdir('../coverage_files/'):
    # print(file)
    if fnmatch.fnmatch(file, '*bam.txt'):
        filtered_coverage_list.append(file)


final_coverage = pd.DataFrame(columns=['I_number', 'numreads', 'coverage', 'meandepth'])

for each in filtered_coverage_list:
    I_number = each.split('-')[0]
    I_number = I_number.replace('-sortedTrimmed.bam.txt', '')
    print(I_number)
    samtools_out = pd.read_table(each, header=0, names=['#rname', 'startpos', 'endpos', 'numreads', 'covbases', 'coverage', 'meandepth', 'meanbaseq', 'meanmapq'])
    samtools_out = samtools_out.assign(I_number=I_number)
    current_coverage = pd.DataFrame(columns=['I_number', 'numreads', 'coverage', 'meandepth'])

    current_coverage['I_number'] = samtools_out['I_number']
    current_coverage['numreads'] = samtools_out['numreads']
    current_coverage['coverage'] = samtools_out['coverage']
    current_coverage['meandepth'] = samtools_out['meandepth']
    print(current_coverage)
    frames = [current_coverage, final_coverage]
    final_coverage = pd.concat(frames)

# final_coverage['I_number'] = I_number_list
final_coverage.to_csv('../freyja_output_processing/coverage_compiled.csv')
