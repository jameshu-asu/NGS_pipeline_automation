import os
import shutil
import argparse
import pandas as pd
import glob
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime
import time
import subprocess
import logging

today_date = datetime.date.today().strftime("%Y%m%d")
readyCheck = False  # Flag that changes when directory is found
targetFastq = ''  # Directory from which fastq files are moved
targetDir = ''  # Directory to which fastq files are moved
qc_file = ''  # Name of respiratory panel QC file
runNumber = 0  # Sequencing run number; obtained from samples file (e.g., Callisto_100)
message_ts = 'NoToken'  # Variable to hold Slack token of primary message in thread
# channel_id = "C02U3BH66AC" #Sequencing workflow
channel_id = "C02RTMZSKPY"  # schtesting
channel_id = "C03969THTHV"  # wastewater_analysis
user_name = "schollan"
agave_server = "agave.asu.edu"

remote_path = '/scratch/%s/wastewater_analysis/' % (user_name)
local_server = 'pluto.biodesign.asu.edu'

parser = argparse.ArgumentParser(
    description='Process sequencing data from Illumina Respiratory Panel')
parser.add_argument('sequencerDirectory', help='Path to sequencer fastq files')
args = parser.parse_args()

print(args)


# def postSlackMessage(slackText):  # Posts a message to slack 'schtesting' channel; checks message_ts variable for thread_ts code, inputting its own if no previous message was sent. Note &,<, and > are protected markup characters
#     slack_token = "xoxb-1091546209987-2889822461282-G03BPjmMGtetLfOURyqlYoQe"
#     client = WebClient(token=slack_token)
#     logger = logging.getLogger(__name__)
#     global message_ts

#     try:
#         if message_ts == 'NoToken':
#             response = client.chat_postMessage(
#                 channel=channel_id,
#                 text=slackText,
#             )
#             print(response)
#             message_ts = response["ts"]

#         else:
#             result = client.chat_postMessage(
#                 channel=channel_id,
#                 thread_ts=message_ts,
#                 text=slackText
#             )

#     except SlackApiError as e:
#         print(f"Error: {e}")


# def postSlackFile(slackText, slackFile):  # Posts a file to the sequencing_workflow channel
#     global message_ts
#     slack_token = "xoxb-1091546209987-2889822461282-G03BPjmMGtetLfOURyqlYoQe"
#     client = WebClient(token=slack_token)
#     try:
#         result = client.files_upload(
#             channels=channel_id,
#             initial_comment=slackText,
#             file=slackFile,
#             thread_ts=message_ts
#         )
#     except SlackApiError as errorRaised:
#         print(errorRaised)
# postSlackMessage('Failed to upload ' + str(slackFile) +
#                  ". Error encountered: " + str(errorRaised))


def checkFile():  # Executes forever, until detection of specified directory, privided by the argument
    sequencerPath = args.sequencerDirectory
    if sequencerPath[-1] != '/':
        sequencerPath = sequencerPath + '/'
    global runNumber
    try:
        csvSampleFile = glob.glob(sequencerPath + '*_*.csv')
        print(csvSampleFile)
        temp = str(csvSampleFile[0])
        dropExt = temp.rstrip('.csv')
        cleanNumber = dropExt.rsplit('_')
        runNumber = cleanNumber[-1]
        # print(temp)
        # print(dropExt)
        # print(runNumber)
        # postSlackMessage('*Wastewater Sequencing Run ' + runNumber + '*')
        # postSlackMessage('Starting search of directory: ' + str(sequencerPath))
    except Exception as e:
        print(e)
        postSlackMessage(
            'Unable to determine run number. Starting search of directory: ' + str(sequencerPath))


# Moves files from sequencing directory -provided in arguments- to current directory.
def copyFiles():
    sequencerPath = args.sequencerDirectory
    if sequencerPath[-1] != '/':
        sequencerPath = sequencerPath + '/'
    global targetDir
    targetDir = str('./')
    global targetFastq
    targetFastq = str('./fastq/')
    try:
        os.makedirs(targetFastq)
    except:
        print('Target directory exists')

    try:
        metadataFile = pd.read_excel('ABCTL Samples.xlsx')
        # Determine which inumbers are Respiratory samples
        wastewater_inumbers = []
        wastewater_sample_name = []
        for index, row in metadataFile.iterrows():
            external_ID = row['External ID']
            external_ID = str(external_ID)
            if external_ID[-3:] == '(2)':
                wastewater_sample_name.append(external_ID)
                wastewater_inumbers.append(row['I_Number'])
        # print(wastewater_inumbers)

        # Determine which Inumbers are present on the current run
        present_samples = glob.glob('%sAnalysis/1/Data/fastq/I*' % (sequencerPath))
        # print(present_samples)

        present_inumbers = []
        for each_path in present_samples:
            each_pair = each_path.split('/')[-1]
            each_inumber = each_pair.split('_')[0]
            # print(each_inumber)
            present_inumbers.append(each_inumber)
        # print(present_inumbers)

        current_wastewater_inumbers = []
        for each_inumber in present_inumbers:
            if each_inumber in wastewater_inumbers:
                current_wastewater_inumbers.append(each_inumber)
        print(current_wastewater_inumbers)

        # Create list of gz file pairs
        gzFiles = []
        for each_inumber in current_wastewater_inumbers:
            file_pairs = glob.glob('%sAnalysis/1/Data/fastq/%s*' % (sequencerPath, each_inumber))
            print(file_pairs)
            for each_item in file_pairs:
                gzFiles.append(each_item)

    # Default: read all gz files
    except:
        gzFiles = glob.iglob(os.path.join(str(sequencerPath) + 'Analysis/1/Data/fastq/', 'I*.gz'))

    print(gzFiles)
    for file in gzFiles:
        shutil.copy(file, targetFastq)
        print(file)
    # postSlackMessage("Files moved to: " + str(os.getcwd()) + ". At " + str(datetime.datetime.now()))


def fasta_preparation():
    preparation_file = glob.glob('QCWorkflow*')
    preparation_file = preparation_file[0]
    subprocess.run('chmod o+x ' + str(targetDir) + preparation_file, shell=True)
    subprocess.run('python ' + str(targetDir) + preparation_file, shell=True)
    preparation_sh = glob.glob('*Respiratory_Workflow.sh')
    preparation_sh = preparation_sh[0].split('/')[-1]
    # postSlackMessage("Respiratory workflow prepared using workflow file '" +
    #                  preparation_file + "'. Now running workflow file '%s'." % (preparation_sh))
    subprocess.run('sh %s' % (preparation_sh), shell=True)
    # postSlackMessage("Reads have been cleaned and mapped. Counts file generation completed.")
    pass


def prepRfiles():
    # Make merge.awk file
    with open('./counts_2022/merge.awk', 'w', newline='') as awk_make:
        awk_make.write('BEGIN {\n')
        awk_make.write('    fname=""\n')
        awk_make.write('    f=0\n')
        awk_make.write('}\n')
        awk_make.write('\n')
        awk_make.write('NR == FNR {\n')
        awk_make.write('    col[NR]=$1\n')
        awk_make.write('    colmax=NR\n')
        awk_make.write('}\n')
        awk_make.write('\n')
        awk_make.write(' { if ( FILENAME != fname ) {\n')
        awk_make.write('     f++\n')
        awk_make.write('     fname=FILENAME\n')
        awk_make.write('     fstrip= split(fname, name_array, "/")\n')
        awk_make.write('     basename=name_array[3]\n')
        awk_make.write('     colfname[f]=basename\n')
        awk_make.write('     }\n')
        awk_make.write('     col2[FNR "-" f]=$3\n')
        awk_make.write(' }\n')
        awk_make.write('\n')
        awk_make.write('END {\n')
        awk_make.write('    for ( j=1 ; j<= f; j++ ) printf "\\t%s",colfname[j]\n')
        awk_make.write('    printf "\\n"\n')
        awk_make.write('    for ( i=1 ; i<=colmax ; i++ ) {\n')
        awk_make.write('    printf "%s",col[i]\n')
        awk_make.write('    for ( j=1 ; j<= f; j++ ) printf "\\t%s",col2[i "-" j]\n')
        awk_make.write('    printf "\\n"\n')
        awk_make.write('    }\n')
        awk_make.write('}')
    # Run awk
    os.system('awk -f ./counts_2022/merge.awk ./counts_2022/I*.txt > ./counts_2022/countsTable.txt')
    readsInOut_file = glob.glob('ReadsInOut*.py')[0]
    os.system('cp ./%s ./logFiles_2022/%s' % (readsInOut_file, readsInOut_file))
    os.system('python ./logFiles_2022/%s' % (readsInOut_file))
    os.makedirs('./r_analysis')

    # Run R script


def main():
    checkFile()
    copyFiles()
    fasta_preparation()
    prepRfiles()


if __name__ == "__main__":
    main()
