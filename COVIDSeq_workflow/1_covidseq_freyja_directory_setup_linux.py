from run import run
import os

'''by James C. Hu
This script will create a run-specific directory structure for COVIDSeq freyja analysis.
Current structure

Root_directory
|- NextSeq1000_###
|  |- bam_files
|  |  |- samtools_coverage.py
|  |- coverage_files
|  |- freyja_output_files
|  |- freyja_output_processing
|  |  |- freyja_compile3.py
|  |  |- freyja_output_dealiasor_grouper.py
'''


def make_freyja_directory():
    os.chdir('../')
    os.chdir(f'NextSeq1000_{run}_Analysis')
    directory_list = ['coverage_files', 'freyja_output_processing']
    for i in directory_list:
        os.mkdir(f'{i}', mode=0o777)
    os.chdir('freyja_output_processing')


make_freyja_directory()
