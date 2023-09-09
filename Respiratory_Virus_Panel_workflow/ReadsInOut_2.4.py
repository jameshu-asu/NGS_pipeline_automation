# Must give files names with samples names only -- one sample name per run files
# All sample log files must be present in directory where the output will be written/script is run from
# Example File (MiSeq)
# WangD-I1672-16817-Tarr-NEC-Pediatric-Stool-352020004-AB46967356
# WangD-I1673-16828-Tarr-NEC-Pediatric-Stool-256010379-AB46963703 
# Usage: 
# 		python readInOut2.py MiSeq124



import sys
import csv
import re
import string
import os.path
import fileinput
import glob

#sys.argv[0]
#FileInput= sys.argv[1]
#name=str(sys.argv[1])+".txt"
#ID= name.split(".")
out="read_metrics.txt"
outfile = str(out)
g = open(outfile,'w')
#file_exists = os.path.isfile("trialOut.txt")
#if not file_exists:
 #   writer.writeheader()

header = ("Sample ID","Adaptor_Trim_Input","AdaptorTrim_Result","PhixRemoved_Input","PhixRemoved_Result","DeDuplicated_Input","DeDuplicated_Result", "Total_Pairs", "Joined","Second_Dedupe_Input","Second_Dedupe_Output", "DeDupe_Merged_Dedupe_Filtered_Input","DeDupe_Merged_Dedupe_Filtered_Output")
g.write("\t".join(header))			## Write output header into file
g.write("\n")
#g.write(" ") #instead of empty it should have sample ID
# ID= name.split(".")
# g.write(ID[0])
# g.write("\t")

#Names=sys.argv[1]
log_files = glob.glob('./logFiles_2022/*-adaptTrimQC*.txt')
Names = []
for each_file in log_files:
	sample_name = each_file.split('-')[0]
	Names.append(sample_name)
print(Names)
for eachsample in Names:
	each_sample_name = eachsample.split('/')[-1]
	each_sample_name = each_sample_name.split('-')[0]
	print(each_sample_name)
	g.write(each_sample_name)
	g.write("\t")
	Filename1=str(eachsample+"-adaptTrimQC_2022.log.txt")
	print(Filename1)
	with open(Filename1, 'r') as file: 
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")
	##Next file parsing (e.g. phix..)
	Filename2=str(eachsample+"phixRemoved_2022.log.txt")
	with open(Filename2, 'r') as file:
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")
	Filename3=str(eachsample+"firstDeduplication.log_2022.txt")
	with open(Filename3, 'r') as file:
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")			
	Filename4=str(eachsample+"firstDeduplicationMerged.log_2022.txt")
	with open(Filename4, 'r') as file:
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")
	Filename5=str(eachsample+"secondDeduplication.log_2022.txt")
	with open(Filename5, 'r') as file:
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")
	Filename6=str(eachsample+"secondDeduplication_filtered.log_2022.txt")
	with open(Filename6, 'r') as file:
		for x in file: 
			if x.startswith("Input:") or x.startswith("Reads Used:") or x.startswith("Pairs:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("Result:") or x.startswith("Joined:"):
				k=x.strip().split("\t") #strip gets rid of last space and split by tab
				#print(k[0])
				l=k[1].split(" ")
				#print(l[0])
				g.write(l[0])
				g.write("\t")
			if x.startswith("ac=f"):
				g.write ("\t")
				g.write ("\n")

	g.write ("\n")
									
									
									
print("parsing adaptor trim complete")
