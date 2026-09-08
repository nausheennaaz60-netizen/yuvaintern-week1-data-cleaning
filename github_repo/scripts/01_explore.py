import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

df = pd.read_csv('penguins_raw.csv')

print("=== SHAPE ===")
print(df.shape)
print("\n=== DTYPES ===")
print(df.dtypes)
print("\n=== MISSING VALUES ===")
print(df.isna().sum())
print("\n=== SEX VALUE COUNTS (check for inconsistent entries) ===")
print(df['Sex'].value_counts(dropna=False))
print("\n=== SPECIES VALUE COUNTS ===")
print(df['Species'].value_counts(dropna=False))
print("\n=== CLUTCH COMPLETION ===")
print(df['Clutch Completion'].value_counts(dropna=False))
print("\n=== NUMERIC SUMMARY ===")
print(df[['Culmen Length (mm)','Culmen Depth (mm)','Flipper Length (mm)','Body Mass (g)']].describe())
print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())
print("\n=== SAMPLE COMMENTS (free text, messy) ===")
print(df['Comments'].dropna().unique()[:5])
