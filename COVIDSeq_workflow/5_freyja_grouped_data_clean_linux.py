from run import run
import pandas as pd
import datetime
import os

'''By James C. Hu
This script will:
1) Update the grouped output with metadata.
'''

#_______Terminal_output_format_______
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 1000)  # pxls
pd.set_option("display.precision", 8)

date = datetime.datetime.now().strftime('%y%m%d')

#____Helper_functions___


def add_col(df_in: pd.DataFrame, col_list: list) -> pd.DataFrame:
    '''This function will:
    1) Add columns from an input list to a dataframe starting at index 0.
    '''
    for i in col_list:
        df_in.insert(0, i, '')
    return df_in


def fetch_data(df_in: pd.DataFrame) -> pd.DataFrame:
    '''This function will:
    1) Generate an output of the updated metadata file.
    '''
    os.chdir('../../../metadata')
    df = pd.read_csv('combined_keys.csv')
    # Tempe
    df_tempe = df[df['Site'].str.startswith('ASUT')]
    df_tempe_freyja = df_tempe[~df_tempe['Sample_ID'].str.endswith('(2)')]
    df_tempe_freyja = df_tempe_freyja.rename(columns={'Seq_ID': 'COVIDSeq_Seq_ID'}).set_index('COVIDSeq_Seq_ID')

    # Poly
    df_polytechnic = df[df['Site'].str.startswith('ASUP')]
    df_polytechnic_freyja = df_polytechnic[~df_polytechnic['Sample_ID'].str.endswith('(2)')]
    df_polytechnic_freyja = df_polytechnic_freyja.rename(columns={'Seq_ID': 'COVIDSeq_Seq_ID'}).set_index('COVIDSeq_Seq_ID')

    # West
    df_west = df[df['Site'].str.startswith('ASUW')]
    df_west_freyja = df_west[~df_west['Sample_ID'].str.endswith('(2)')]
    df_west_freyja = df_west_freyja.rename(columns={'Seq_ID': 'COVIDSeq_Seq_ID'}).set_index('COVIDSeq_Seq_ID')

    # Downtown
    df_downtown = df[df['Site'].str.startswith('ASUDT')]
    df_downtown_freyja = df_downtown[~df_downtown['Sample_ID'].str.endswith('(2)')]
    df_downtown_freyja = df_downtown_freyja.rename(columns={'Seq_ID': 'COVIDSeq_Seq_ID'}).set_index('COVIDSeq_Seq_ID')

    # cd back to working dir/output dir
    os.chdir('output_for_streamlit')
    # Preparing updated grouped file
    df_out = df_in
    df_out.update(df_tempe_freyja)
    df_out.update(df_polytechnic_freyja)
    df_out.update(df_west_freyja)
    df_out.update(df_downtown_freyja)
    df_out['Date'] = df_out['Date'].astype(str).str.split('.').str[0]
    return df_out


add_col_list = ['Site', 'Date', 'Sample_ID']

df = pd.read_csv(f'/mnt/storage/wastewater_analysis/coronavirus/freyja/NextSeq1000_{run}_Analysis/freyja_output_processing/freyja_grouped_{run}.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.rename(columns={'lineages': 'COVIDSeq_Seq_ID'})
df = df.set_index('COVIDSeq_Seq_ID')
df['Filtered_reads'] = 1 - df.sum(axis=1)
df = add_col(df, add_col_list)
df = fetch_data(df)

df.to_csv(f'freyja_grouped_metadata_analysis_{run}.csv')
