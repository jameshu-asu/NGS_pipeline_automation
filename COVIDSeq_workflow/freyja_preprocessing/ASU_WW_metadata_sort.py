import pandas as pd
import numpy as np
import datetime
from openpyxl import load_workbook
import os

#_______Terminal_output_format_______
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 1000)  # pxls
pd.set_option("display.precision", 8)



# Tempe
df_tempe = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Tempe', usecols='AH, AJ, AL, AM')
df_tempe_freyja = df_tempe.rename(columns={'COVIDSeq Seq ID': 'Seq_ID', 'ABCTL CovSeq Code': 'Sample_ID', 'Date.1':'Date', 'Location Code.1':'Site'})
df_tempe_freyja = df_tempe_freyja.dropna(axis=0)
df_tempe_freyja['Date'] = df_tempe_freyja['Date'].astype(float)
df_tempe_freyja = df_tempe_freyja.drop_duplicates()
df_tempe_freyja = df_tempe_freyja.set_index('Seq_ID')

df_tempe = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Tempe', usecols='AI, AK, AL, AM')
df_tempe_RVP = df_tempe.rename(columns={'Respiratory Seq ID': 'Seq_ID', 'ABCTL RVP Code': 'Sample_ID', 'Date.1':'Date', 'Location Code.1':'Site'})
df_tempe_RVP = df_tempe_RVP.dropna(axis=0)
df_tempe_RVP['Date'] = df_tempe_RVP['Date'].astype(float)
df_tempe_RVP = df_tempe_RVP.drop_duplicates()
df_tempe_RVP = df_tempe_RVP.set_index('Seq_ID')

# print(df_tempe_freyja)
# print(df_tempe_RVP)


# Poly
df_poly = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Polytech', usecols='AJ, AL, AN, AO')
df_poly_freyja = df_poly.rename(columns={'COVIDSeq Seq ID': 'Seq_ID', 'ABCTL CovSeq Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_poly_freyja = df_poly_freyja.dropna(axis=0)
df_poly_freyja['Date'] = df_poly_freyja['Date'].astype(float)
df_poly_freyja = df_poly_freyja.drop_duplicates()
df_poly_freyja = df_poly_freyja.set_index('Seq_ID')

df_poly = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Polytech', usecols='AK, AM, AN, AO')
df_poly_RVP = df_poly.rename(columns={'Respiratory Seq ID': 'Seq_ID', 'ABCTL RVP Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_poly_RVP = df_poly_RVP.dropna(axis=0)
df_poly_RVP['Date'] = df_poly_RVP['Date'].astype(float)
df_poly_RVP = df_poly_RVP.drop_duplicates()
df_poly_RVP = df_poly_RVP.set_index('Seq_ID')

# print(df_poly_freyja)
# print(df_poly_RVP)

# West
df_west = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='West', usecols='AJ, AL, AN, AO')
df_west_freyja = df_west.rename(columns={'COVIDSeq Seq ID': 'Seq_ID', 'ABCTL CovSeq Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_west_freyja = df_west_freyja.dropna(axis=0)
df_west_freyja['Date'] = df_west_freyja['Date'].astype(float)
df_west_freyja = df_west_freyja.drop_duplicates()
df_west_freyja = df_west_freyja.set_index('Seq_ID')

df_west = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='West', usecols='AK, AM, AN, AO')
df_west_RVP = df_west.rename(columns={'Respiratory Seq ID': 'Seq_ID', 'ABCTL RVP Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_west_RVP = df_west_RVP.dropna(axis=0)
df_west_RVP['Date'] = df_west_RVP['Date'].astype(float)
df_west_RVP = df_west_RVP.drop_duplicates()
df_west_RVP = df_west_RVP.set_index('Seq_ID')

# print(df_west_freyja)
# print(df_west_RVP)

# Downtown
df_dt = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Downtown', usecols='AJ, AL, AN, AO')
df_dt_freyja = df_dt.rename(columns={'COVIDSeq Seq ID': 'Seq_ID', 'ABCTL CovSeq Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_dt_freyja = df_dt_freyja.dropna(axis=0)
df_dt_freyja['Date'] = df_dt_freyja['Date'].astype(float)
df_dt_freyja = df_dt_freyja.drop_duplicates()
df_dt_freyja = df_dt_freyja.set_index('Seq_ID')

df_dt = pd.read_excel('ASU_WW_Sample_Metadata_james_copy.xlsx', sheet_name='Downtown', usecols='AK, AM, AN, AO')
df_dt_RVP = df_dt.rename(columns={'Respiratory Seq ID': 'Seq_ID', 'ABCTL RVP Code': 'Sample_ID', 'Date.1':'Date', 'Location Code':'Site'})
df_dt_RVP = df_dt_RVP.dropna(axis=0)
df_dt_RVP['Date'] = df_dt_RVP['Date'].astype(float)
df_dt_RVP = df_dt_RVP.drop_duplicates()
df_dt_RVP = df_dt_RVP.set_index('Seq_ID')

# print(df_dt_freyja)
# print(df_dt_RVP)

df_combined = pd.concat([df_tempe_freyja, df_tempe_RVP, df_poly_freyja, df_poly_RVP, df_west_freyja, df_west_RVP, df_dt_freyja, df_dt_RVP])

os.chdir('../../../../metadata')

df_combined.to_csv('combined_keys.csv')

