import subprocess

'''By James C. Hu
This script will:
1) Orchestrate the COVIDSeq workflow.
'''

# Name the sequencing run extension.
run = 'TWW'

print('Creating directory structure for analysis. Running script 1.')
subprocess.call(['python', '1_covidseq_freyja_directory_setup_linux.py'])

print('Directory created. Compiling sequencing data. Running script 2.')
subprocess.call(['python', '2_freyja_compile4_linux.py'])

print('Sequencing data compiled. Dealiasing sequencing data. Running script 3 ')
subprocess.call(['python', '3_freyja_output_dealiasor_grouper_linux.py'])

print('Sequences dealiased. QC-ing dealiased data. Running script 4')
subprocess.call(['python', '4_samtools_coverage2_linux.py'])

print('Sequence QC complete. Preparing output for visualization. Running script 5 ')
subprocess.call(['python', '5_freyja_grouped_data_clean_linux.py'])

print('Merging output to combined file. Running script 6')
subprocess.call(['python', '6_merge_data_linux.py'])
