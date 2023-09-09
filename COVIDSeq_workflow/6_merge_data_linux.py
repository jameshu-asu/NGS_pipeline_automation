from run import run
import pandas as pd
import datetime
import os

'''By James C. Hu
This script will:
1) Generate outputs for the streamlit dashboard.
'''

#_______Terminal_output_format_______
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 1000)  # pxls
pd.set_option("display.precision", 8)

date = datetime.datetime.now().strftime('%y%m%d')

os.chdir('../../../metadata/output_for_streamlit')

#___Merging_to_combined___
in1 = 'Combined_freyja_grouped_metadata_analysis_230324.csv'
in2 = f'freyja_grouped_metadata_analysis_{run}.csv'
out1 = f'Combined_freyja_grouped_metadata_analysis_{date}.csv'

df_in1 = pd.read_csv(in1).set_index('COVIDSeq_Seq_ID')
df_in2 = pd.read_csv(in2).set_index('COVIDSeq_Seq_ID')

print(df_in1.head())
print(df_in2.head())

combined_df = pd.concat([df_in1, df_in2])
combined_df = combined_df.drop_duplicates()
combined_df.to_csv(out1, mode='w', header=True)


print('Shape of original combined df')
print(df_in1.shape)
print('Shape of df being added')
print(df_in2.shape)
print('Shape of new combined df')
print(combined_df.shape)
