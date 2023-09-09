from run import run
import csv
import pandas as pd
import os
import fnmatch

os.chdir(f'../NextSeq1000_{run}_Analysis/freyja_output_processing')

# Find and compile Freyja output file names
path = (f'../freyja_output_files')
file_list = []
for file in os.listdir(path):
    if fnmatch.fnmatch(file, 'I*'):
        file_list.append(file)


# generate .csv file consisting of freyja_output filenames
with open(f'freyja_output_file_list_{run}.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter='\n')
    writer.writerow(file_list)

df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
df4 = pd.DataFrame()

# Parse each freyja output file, generating list of lineages, lineage abundances, summary lineages, and summary lineage abundances
file_list = str(f'freyja_output_file_list_{run}.csv')
with open(file_list, 'r') as read_list:
    for each_file in read_list:
        each_file = each_file.replace("\n", "")
        infile1 = each_file.strip().split('_')
        inumber = infile1[0]

        sampleid = inumber
        newline = sampleid
        lineage_list = []
        abundance_list = []

        summarylist = []
        summary_lineage_list = []
        summary_abundance_list = []
        emptylist = []
        parselist = []

# move to directory containing freyja_output files for reading
        if str(os.getcwd()) != path:
            os.chdir(path)
# populate parselist with each freya_output file as single entry in list
        with open(infile1[0] + '_freyja_output', 'r') as file:
            for line in file:
                if line.startswith("lineages"):
                    parselist.append(newline)
                    newline = line.strip()
                    newline += " "
                elif line.startswith("summarized"):
                    parselist.append(newline)
                    newline = line.strip()
                    newline += " "
                elif line.startswith("abundances"):
                    parselist.append(newline)
                    newline = line.strip()
                    newline += " "
                elif line.startswith("resid"):
                    parselist.append(newline)
                    newline = line.strip()
                    newline += " "
                else:
                    newline += line.strip()
                    newline += " "
            parselist.append(newline)
            newline += line.replace("\n", " ")

            (parselist)
            print()

            # Convert lineages into a str list
        print(parselist[2])
        newline = parselist[2]
        newline = newline.strip()
        newline = newline.replace("'", "")
        newline = newline.replace('"', "")
        newline = newline.replace("[", "")
        newline = newline.replace("]", "")
        newline = newline.replace("\t", " ")
        newline = newline.replace("\n", " ")
        newline = newline.split(" ")
        for eachlineage in newline:
            lineage_list.append(eachlineage)

        while("" in lineage_list):
            lineage_list.remove("")
        print()
        print(lineage_list)

        print()
        print(parselist[3])
        newline = parselist[3]
        newline = newline.strip()
        newline = newline.replace("'", "")
        newline = newline.replace('"', "")
        newline = newline.replace("[", "")
        newline = newline.replace("]", "")
        newline = newline.replace("\t", " ")
        newline = newline.replace("\n", " ")
        newline = newline.split(" ")
        for eachabundance in newline:
            abundance_list.append(eachabundance)

        while("" in abundance_list):
            abundance_list.remove("")
        print()
        print(abundance_list)
        abundance_list[0] = sampleid
        print()
        print(newline)
        print()
        print(len(lineage_list))
        print(lineage_list)
        print()
        print(len(abundance_list))
        print(abundance_list)
        df2 = pd.DataFrame({lineage_list[0]: lineage_list[1:], abundance_list[0]: abundance_list[1:]})
        df2 = df2.set_index('lineages')

        df1 = pd.concat([df1, df2], axis=1, join="outer")

        ###Summary Lineages###
        newline = parselist[1]

        newline = newline.strip().split("\t")
        newline = newline[1]
        newline = newline.replace("('BA.2* [Omicron (BA.2.X)]'", "(BA.2*OmicronBA.2.X")
        newline = newline.replace("('BA.5* [Omicron (BA.5.X)]'", "(BA.5*OmicronBA.5.X")
        newline = newline.replace("('BA.2.75* [Omicron (BA.2.75.X)]'", "(BA.2.75*OmicronBA.2.75.X")
        newline = newline.replace("('BQ.1* [Omicron (BQ.1.X)]'", "(BQ.1*OmicronBQ.1.X")
        newline = newline.replace("('XBB.1.5* [Omicron (XBB.1.5.X)]'", "(XBB.1.5*OmicronXBB.1.5.X")
        newline = newline.replace("[", "")
        newline = newline.replace("]", "")
        newline = newline.replace("'", "")
        newline = newline.replace("),", ");")
        newline = newline.split(";")

        for i in newline:

            i = i.replace("(", "")
            i = i.replace(")", "")
            i = i.replace(" ", "")
            i = i.split(",")
            summary_lineage_list.append(i)

        if (len(summary_lineage_list)) > 1:
            df3 = pd.DataFrame(summary_lineage_list, columns=['lineage', inumber])

        else:
            if len(i) == 1:
                df3 = pd.DataFrame(emptylist, columns=['lineage', inumber])
            else:
                df3 = pd.DataFrame(summary_lineage_list, columns=['lineage', inumber])

        df3 = df3.set_index('lineage')
        df4 = pd.concat([df4, df3], axis=1, join="outer")

os.chdir('../freyja_output_processing')
df4.to_csv(f"freyja_output_all_summaries1_{run}.csv", index=True)
df1.to_csv(f"freyja_output_all_lineages1_{run}.csv", index=True)
