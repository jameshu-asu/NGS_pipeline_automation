from run import run
import pandas as pd
import os
from pango_aliasor.aliasor import Aliasor


os.chdir(f'../NextSeq1000_{run}_Analysis/freyja_output_processing')

aliasor = Aliasor()

# Read compiled freyja lineage output into pandas dataframe
freyja_aliased_df = pd.read_csv(f"freyja_output_all_lineages1_{run}.csv")
freyja_aliased_df.set_index("lineages")

# add all aliased lineages in aliased dataframe to aliased list, add all i_numbers to i_number_list
aliased_list = freyja_aliased_df.loc[:, ("lineages")]  # create list from all values in lineage column of freyja_aliased_df
dealiased_list = []  # create empty list to hold dealiased lineages
i_number_list = list(freyja_aliased_df.columns)  # create list containing all i_numbers present in column headers of freyja_aliased_df
i_number_list.remove('lineages')  # remove lineage header from i_number_list

# Create empty dataframe to populate with de-aliased lineages and relative abundance values for each inumber, set inumber columns
freyja_dealiased_df = pd.DataFrame(columns=freyja_aliased_df.columns)  # set column names of freyja_dealiased_df to column names present in freyja_aliased_df (i_numbers)

# Loop through rows of freyja_aliased_df, passing aliased lineages through dealiasor, add dealiased lineages to list
for lineage in aliased_list:
    dealiased = aliasor.uncompress(lineage)  # ex. from BA.2 to B.1.1.529.2
    dealiased_list.append(dealiased)  # add each dealiased lineage to dealiased list


# populate lineages column of dealiased dataframe with dealiased lineages in dealiased list
freyja_dealiased_df.loc[:, ("lineages")] = dealiased_list


# copy all relative abundance values from aliased dataframe to dealiased dataframe
freyja_dealiased_df.iloc[:, 1:] = freyja_aliased_df.iloc[:, 1:]  # copy values from all rows, all columns from integer index 1 to end from aliased_df to dealiased_df (abundance values)

# transpose dealiased dataframe for i_number rows, lineage columns
freyja_dealiased_df_transposed = freyja_dealiased_df.T
freyja_dealiased_df_transposed = freyja_dealiased_df_transposed.rename_axis('lineages').reset_index()

new_header = freyja_dealiased_df_transposed.iloc[0]  # grab the first row for the header
freyja_dealiased_df_transposed = freyja_dealiased_df_transposed[1:]  # take the data less the header row
freyja_dealiased_df_transposed.columns = new_header  # set the header row as the df header
# print(freyja_dealiased_df_transposed)


# write intermediate dataframes to csv files
freyja_dealiased_df_transposed.to_csv(f"dealiased_transposed_{run}.csv")
freyja_aliased_df.to_csv(f"aliased_lineages_{run}.csv")
freyja_dealiased_df.to_csv(f"dealiased_lineages_{run}.csv")

# following chunk only necessary to properly format output of variable column in freyja_dealiased_df_transposed_melted
# without, variable column filled with index values
# Not using melted table, commenting out for now
# lineage_columns = list(freyja_dealiased_df_transposed.iloc[0,0:]) #create a list, lineage_columns, from column headers in freyja_dealiased_transposed
# freyja_dealiased_df_transposed.columns = lineage_columns #set column labels in freyja_dealiased_df_transposed to lineages in lineage_columns list
# freyja_dealiased_df_transposed_melted = freyja_dealiased_df_transposed.melt(id_vars = 'lineages') #create new long dataframe freyja_dealiased_df_transposed_melted from wide dataframe freyja_dealiased_df_transposed

# freyja_dealiased_df_transposed_melted.to_csv("dealiased_transposed_melted.csv")

# ###Create dataframe for grouped abundances
# Currently not creating final dataframe with this strategy
# freyja_grouped_df = pd.DataFrame(columns = ('i_number', 'BQ.1.1', 'XBB.1.5','BQ.1','XBB','BA.5','BN.1','BF.7','BA.2.75','BA.5.2.6','BA.2','BF.11','BA.4.6','BA.2','BA.2.75.2','BA.4','BA.1.1','B.1.1.529','BA.2.12.1','B.1.617.2','Other'))
# freyja_grouped_df = freyja_grouped_df.reset_index(drop = True)
# freyja_grouped_df.to_csv("freyja_grouped.csv")

# print(freyja_dealiased_df_transposed_melted)
# for each in i_number_list:
# 	grouped = freyja_dealiased_df_transposed_melted.groupby("lineages")
# 	print(grouped)


# Describe pattern matching, sum abundances for grouped categories by sample(use CDC nowcast as template)

freyja_grouped_df = freyja_dealiased_df_transposed  # new dataframe to house grouped data

# BQ.1.1*
#'B.1.1.529.5.3.1.1.1.1.1.1'
BQ11_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.3.1.1.1.1.1.1') or each == 'B.1.1.529.5.3.1.1.1.1.1.1':  # Add BQ.1.1 and sublineages to BQ11_list
        BQ11_list.append(each)

freyja_grouped_df['BQ.1.1'] = freyja_grouped_df[BQ11_list].sum(axis=1)  # Merge lineages in BQ11_list into BQ.1.1
freyja_grouped_df = freyja_grouped_df.drop(BQ11_list, axis=1)    # Drop all the lineages in BQ11_list after merging

# XBB.1.5
#'XBB.1.5'
XBB15_list = []
for each in dealiased_list:
    if each.startswith('XBB.1.5') or each == 'XBB.1.5':  # Add XBB.1.5 and sublineages to XBB.1.5 list
        XBB15_list.append(each)

freyja_grouped_df['XBB15grouped'] = freyja_grouped_df[XBB15_list].sum(axis=1)  # Merge lineages in XBB15_list into XBB.1.5
freyja_grouped_df = freyja_grouped_df.drop(XBB15_list, axis=1)    # Drop all the lineages in XBB15_list after merging
freyja_grouped_df = freyja_grouped_df.rename(columns={'XBB15grouped': 'XBB.1.5'})  # rename XBB grouped to XBB
print(XBB15_list)

# BQ.1
#'B.1.1.529.5.3.1.1.1.1.1' (NOT 'B.1.1.529.5.3.1.1.1.1.1.1'/ BQ.1.1 sublineages)
BQ1_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.3.1.1.1.1.1') or each == 'B.1.1.529.5.3.1.1.1.1.1':  # Add BQ.1 and sublineages to BQ1_list
        BQ1_list.append(each)

BQ1_exclusion_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.3.1.1.1.1.1.1') or each == 'B.1.1.529.5.3.1.1.1.1.1.1':  # Add BQ.1.1 and sublineages to BQ1_exclusion list
        BQ1_exclusion_list.append(each)

for each in BQ1_exclusion_list:
    if each in BQ1_list:  # Remove all lineages in BQ.1 exclusion list from BQ.1 list
        BQ1_list.remove(each)

freyja_grouped_df['BQ.1'] = freyja_grouped_df[BQ1_list].sum(axis=1)  # Merge lineages in BQ1_list into BQ.1
freyja_grouped_df = freyja_grouped_df.drop(BQ1_list, axis=1)    # Drop all the lineages in BQ.1_list after merging

# XBB
#'XBB'
# include 'XBB*' (NOT XBB.1.5)
XBB_list = []
for each in dealiased_list:
    if each.startswith('XBB') or each == 'XBB':  # Add XBB and sublineages to XBB_list
        XBB_list.append(each)

XBB_exclusion_list = []
for each in dealiased_list:
    if each.startswith('XBB.1.5') or each == 'XBB.1.5':  # Add XBB.1.5 and sublineages to XBB_exclusion_list
        XBB_exclusion_list.append(each)

for each in XBB_exclusion_list:
    if each in XBB_list:  # Remove all lineages in XBB_exclusion_list from XBB list
        XBB_list.remove(each)

freyja_grouped_df['XBBgrouped'] = freyja_grouped_df[XBB_list].sum(axis=1)  # merge lianges in XBB_list into XBBgrouped
freyja_grouped_df = freyja_grouped_df.drop(XBB_list, axis=1)  # Drop all the lineages in XBB_list after merging
freyja_grouped_df = freyja_grouped_df.rename(columns={'XBBgrouped': 'XBB'})  # rename XBB grouped to XBB


# BA.5
#'B.1.1.529.5'
# include 'B.1.1.529.5*' (NOT 'B.1.1.529.5.2.1.7'/'BF.7', 'B.1.1.529.5.2.1.11'/'BF.11', 'B.1.1.529.5.2.6'/'BA.5.2.6', 'B.1.1.529.5.3.1.1.1.1.1'/'BQ.1', 'B.1.1.529.5.3.1.1.1.1.1.1'/'BQ.1.1')
BA5_list = []
for each in dealiased_list:
    if each.startswith("B.1.1.529.5") or each == "B.1.1.529.5":  # Add BA.5 and sublineages to BA.5 list
        BA5_list.append(each)

BA5_exclusion_list = []
for each in BA5_list:
    if each.startswith('B.1.1.529.5.2.1.7') or each == 'B.1.1.529.5.2.1.7':  # Add BF.7 and sublineages to BA.5 exclusion list
        BA5_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.5.2.1.11') or each == 'B.1.1.529.5.2.1.11':  # Add BF.11 and sublineages to BA.5 exclusion list
        BA5_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.5.2.6') or each == 'B.1.1.529.5.2.6':  # Add BA.5.2.6 and sublineages to BA.5 exclusion list
        BA5_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.5.3.1.1.1.1.1') or each == 'B.1.1.529.5.3.1.1.1.1.1':  # Add BQ.1 and sublineages to BA.5 exclusion list
        BA5_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.5.3.1.1.1.1.1.1') or each == 'B.1.1.529.5.3.1.1.1.1.1.1':  # Add BQ.1.1 and sublineages to BA.5 exclusion list
        BA5_exclusion_list.append(each)

for each in BA5_exclusion_list:
    if each in BA5_list:  # Remove all BA.5 sublineages in exclusion list from BA.5 list
        BA5_list.remove(each)

freyja_grouped_df['BA.5'] = freyja_grouped_df[BA5_list].sum(axis=1)      # Merge lineanges in BA5_list into BA.5
freyja_grouped_df = freyja_grouped_df.drop(BA5_list, axis=1)    # Drop all the lineages in BA5_list after merging


# BN.1
#'B.1.1.529.2.75.5.1'
BN1_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.2.75.5.1') or each == 'B.1.1.529.2.75.5.1':  # Add BN.1 and sublineages to BN1_list
        BN1_list.append(each)

freyja_grouped_df['BN.1'] = freyja_grouped_df[BN1_list].sum(axis=1)  # Merge lineages in BN1_list into BN.1
freyja_grouped_df = freyja_grouped_df.drop(BN1_list, axis=1)    # Drop all the lineages in BN1_list after merging


# BF.7
#'B.1.1.529.5.2.1.7'
BF7_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.2.1.7') or each == 'B.1.1.529.5.2.1.7':  # Add BF.7 and sublineages to BF7_list
        BF7_list.append(each)

freyja_grouped_df['BF.7'] = freyja_grouped_df[BF7_list].sum(axis=1)  # Merge lineages in BF7_list into BF.7
freyja_grouped_df = freyja_grouped_df.drop(BF7_list, axis=1)  # Drop all the lineages in BF7_list after merging

# BA.2.75
#'B.1.1.529.2.75'
BA275_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.2.75') or each == 'B.1.1.529.2.75':  # Add BA.2.75 and sublineages to BA275_list
        BA275_list.append(each)

BA275_exclusion_list = []
for each in BA275_list:
    if each.startswith('B.1.1.529.2.75.2') or each == 'B.1.1.529.2.75.2':
        BA275_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.2.75.5.1') or each == 'B.1.1.529.2.75.5.1':
        BA275_exclusion_list.append(each)


for each in BA275_exclusion_list:
    if each in BA275_list:  # Remove all BA.2.75 sublineages in exclusion list from BA.2.75 list
        BA275_list.remove(each)

freyja_grouped_df['BA.2.75'] = freyja_grouped_df[BA275_list].sum(axis=1)  # Merge lineages in BA275_list into BA.2.75
freyja_grouped_df = freyja_grouped_df.drop(BA275_list, axis=1)    # Drop all the lineages in BA275_list after merging

# BA.5.2.6
#'B.1.1.529.5.2.6'
BA526_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.2.6') or each == 'B.1.1.529.5.2.6':
        BA526_list.append(each)

freyja_grouped_df['BA.5.2.6'] = freyja_grouped_df[BA526_list].sum(axis=1)  # Merge lineages in BA526_list into BA.5.2.6
freyja_grouped_df = freyja_grouped_df.drop(BA526_list, axis=1)    # Drop all the lineages in BA526_list after merging

# BF.11
#'B.1.1.529.5.2.1.11'
BF11_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.5.2.1.11') or each == 'B.1.1.529.5.2.1.11':  # Add BF.11 and sublineages to BF11_list
        BF11_list.append(each)

freyja_grouped_df['BF.11'] = freyja_grouped_df[BF11_list].sum(axis=1)  # Merge lineages in BF11_list into BF.11
freyja_grouped_df = freyja_grouped_df.drop(BF11_list, axis=1)    # Drop all the lineages in BF11_list after merging

# BA.4.6
#'B.1.1.529.4.6'
BA46_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.4.6') or each == 'B.1.1.529.4.6':  # Add BA.4.6 and sublineages to BA46_list
        BA46_list.append(each)

freyja_grouped_df['BA.4.6'] = freyja_grouped_df[BA46_list].sum(axis=1)  # Merge lineages in BA46_list into BA.4.6
freyja_grouped_df = freyja_grouped_df.drop(BA46_list, axis=1)    # Drop all the lineages in BA46_list after merging

# BA.2
#'B.1.1.529.2'
# include 'B.1.1.529.2' (NOT 'B.1.1.529.2.12.1'/ BA.2.12.1, 'B.1.1.529.2.75.2'/ BA.2.75.2, 'B.1.1.529.2.75'/ BA.2.75, 'B.1.1.529.2.75.5.1'/ BN.1, 'XBB')
BA2_list = []
for each in dealiased_list:
    if each.startswith("B.1.1.529.2") or each == "B.1.1.529.2":  # Add BA.2 and sublineages to BA2_list
        BA2_list.append(each)

BA2_exclusion_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.2.12.1') or each == 'B.1.1.529.2.12.1':
        BA2_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.2.75.2') or each == 'B.1.1.529.2.75.2':
        BA2_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.2.75') or each == 'B.1.1.529.2.75':
        BA2_exclusion_list.append(each)
    elif each.startswith('B.1.1.529.2.75.5.1') or each == 'B.1.1.529.2.75.5.1':
        BA2_exclusion_list.append(each)
    elif each.startswith('XBB') or each == 'XBB':
        BA2_exclusion_list.append(each)

for each in BA2_exclusion_list:
    if each in BA2_list:  # Remove all BA.2 sublineages in exclusion list from BA.2 list
        BA2_list.remove(each)

freyja_grouped_df['BA.2'] = freyja_grouped_df[BA2_list].sum(axis=1)  # merge lineanges in BA2_list into BA.2
freyja_grouped_df = freyja_grouped_df.drop(BA2_list, axis=1)  # Drop all the lineages in BA2_list after merging

# BA.2.75.2
#'B.1.1.529.2.75.2'
BA2752_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.2.75.2') or each == 'B.1.1.529.2.75.2':
        BA2752_list.append(each)

freyja_grouped_df['BA.2.75.2'] = freyja_grouped_df[BA2752_list].sum(axis=1)  # merge lineages in BA2752_list into BA.2.75.2
freyja_grouped_df = freyja_grouped_df.drop(BA2752_list, axis=1)  # Drop all the lineages in BA2752_list after merging

# BA.4
#'B.1.1.529.4' (NOT B.1.1.529.4.6)
BA4_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.4') or each == 'B.1.1.529.4':
        BA4_list.append(each)

BA4_exclusion_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.4.6') or each == 'B.1.1.529.4.6':
        BA4_exclusion_list.append(each)

for each in BA4_exclusion_list:
    if each in BA4_list:
        BA4_list.remove(each)

freyja_grouped_df['BA.4'] = freyja_grouped_df[BA4_list].sum(axis=1)  # merge lineanges in BA2_list into BA.2
freyja_grouped_df = freyja_grouped_df.drop(BA4_list, axis=1)  # Drop all the lineages in BA2_list after merging

# BA.1.1
#'B.1.1.529.1.1'
# include 'B.1.1.529.1.1*'
BA11_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.1.1') or each == 'B.1.1.529.1.1':
        BA11_list.append(each)

freyja_grouped_df['BA.1.1'] = freyja_grouped_df[BA11_list].sum(axis=1)  # merge lineanges in BA11_list into BA.1.1
freyja_grouped_df = freyja_grouped_df.drop(BA11_list, axis=1)  # Drop all the lineages in BA11_list after merging

# B.1.1.529
#'B.1.1.529'
# include 'B.1.1.529.1' (NOT 'B.1.1.529.1.1'), 'B.1.1.529.3'
B11529_list = []
for each in dealiased_list:
    if each.startswith("B.1.1.529.1") or each == "B.1.1.529.1":
        B11529_list.append(each)
    elif each.startswith("B.1.1.529.3") or each == "B.1.1.529.3":
        B11529_list.append(each)

B11529_exclusion_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.1.1') or each == 'B.1.1.529.1.1':
        B11529_list.remove(each)

for each in B11529_exclusion_list:
    if each in B11529_list:
        B11529_list.remove(each)

freyja_grouped_df['B.1.1.529'] = freyja_grouped_df[B11529_list].sum(axis=1)  # merge lineanges in B11529_list into B.1.1.529
freyja_grouped_df = freyja_grouped_df.drop(B11529_list, axis=1)  # Drop all the lineages in B11529_list after merging

# BA.2.12.1
#'B.1.1.529.2.12.1'
BA2121_list = []
for each in dealiased_list:
    if each.startswith('B.1.1.529.2.12.1') or each == 'B.1.1.529.2.12.1':
        BA2121_list.append(each)

freyja_grouped_df['BA.2.12.1'] = freyja_grouped_df[BA2121_list].sum(axis=1)  # merge lineages in BA2121_list into BA.2.12.1
freyja_grouped_df = freyja_grouped_df.drop(BA2121_list, axis=1)  # Drop all the lineages in BA2121_list after merging

# B.1.617.2
#'B.1.617.2'
B16172_list = []
for each in dealiased_list:
    if each.startswith('B.1.617.2') or each == 'B.1.617.2':
        B16172_list.append(each)

freyja_grouped_df['B.1.617.2grouped'] = freyja_grouped_df[B16172_list].sum(axis=1)  # merge lineages in B16172_list into BA.2.75.2
freyja_grouped_df = freyja_grouped_df.drop(B16172_list, axis=1)  # Drop all the lineages in B16172_list after merging
freyja_grouped_df = freyja_grouped_df.rename(columns={'B.1.617.2grouped': 'Delta'})  # rename B.1.617.2grouped to Delta

# Other Recombinant
other_recombinant_list = []  # create list to house all other recombinant lineages
for each in dealiased_list:
    if each.startswith('X'):
        other_recombinant_list.append(each)

other_recombinant_exclusion_list = XBB_list + XBB15_list

for each in other_recombinant_exclusion_list:
    if each in other_recombinant_list:
        other_recombinant_list.remove(each)

freyja_grouped_df['Other_recombinants'] = freyja_grouped_df[other_recombinant_list].sum(axis=1)  # merge lineanges in other_list into Other
freyja_grouped_df = freyja_grouped_df.drop(other_recombinant_list, axis=1)  # Drop all the lineages in other_list after merging
freyja_grouped_df.to_csv(f'freyja_grouped_{run}.csv')

# Other
other_list = dealiased_list  # create list to house all other lineages
LOI_combined_list = []  # create list with all lineages used for final grouped columns
LOI_combined_list = BQ11_list + XBB15_list + BQ1_list + XBB_list + BA5_list + BN1_list + BF7_list + BA275_list + BA526_list + BF11_list + BA46_list + BA2_list + BA2752_list + BA4_list + BA11_list + B11529_list + BA2121_list + B16172_list + other_recombinant_list

for each in LOI_combined_list:
    if each in other_list:
        other_list.remove(each)

freyja_grouped_df['Other'] = freyja_grouped_df[other_list].sum(axis=1)  # merge lineanges in other_list into Other
freyja_grouped_df = freyja_grouped_df.drop(other_list, axis=1)  # Drop all the lineages in other_list after merging
freyja_grouped_df.to_csv(f'freyja_grouped_{run}.csv')
