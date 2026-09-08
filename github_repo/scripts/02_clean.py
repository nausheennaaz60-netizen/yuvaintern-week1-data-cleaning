import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 120

df = pd.read_csv('penguins_raw.csv')

numeric_cols = ['Culmen Length (mm)', 'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)']

# ---------- SCREENSHOT 1: Missing value heatmap (before cleaning) ----------
plt.figure(figsize=(10, 5))
sns.heatmap(df.isna(), cbar=False, cmap='Reds', yticklabels=False)
plt.title('Missing Values Before Cleaning')
plt.tight_layout()
plt.savefig('shot1_missing_before.png')
plt.close()

# ---------- SCREENSHOT 2: Boxplots to inspect outliers ----------
fig, axes = plt.subplots(1, 4, figsize=(14, 4))
for ax, col in zip(axes, numeric_cols):
    sns.boxplot(y=df[col], ax=ax, color='steelblue')
    ax.set_title(col, fontsize=9)
plt.tight_layout()
plt.savefig('shot2_boxplots_before.png')
plt.close()

# ================= CLEANING STEPS =================

# Step 1: Standardize inconsistent text casing in Species
df['Species'] = df['Species'].str.replace('Adelie Penguin', 'Adelie penguin', regex=False)

# Step 2: Drop rows missing ALL four core physical measurements (2 rows -
# these represent penguins that could not be measured at all, so imputing
# would fabricate data rather than clean it)
before_rows = len(df)
df = df.dropna(subset=numeric_cols, how='all')
after_rows = len(df)

# Step 3: Handle missing Sex values -> keep as explicit category rather than
# guessing; guessing sex from morphometrics would introduce bias into a
# column that may itself be an analysis target
df['Sex'] = df['Sex'].fillna('Unknown')

# Step 4: Handle missing isotope columns (Delta 15 N, Delta 13 C) ->
# median imputation per species, since these are chemical measurements
# with species-level baseline differences
for col in ['Delta 15 N (o/oo)', 'Delta 13 C (o/oo)']:
    df[col] = df.groupby('Species')[col].transform(lambda x: x.fillna(x.median()))

# Step 5: Comments column is 84% missing free text and not used in
# quantitative analysis -> leave as-is but flag has_comment for reference
df['has_comment'] = df['Comments'].notna()

# Step 6: Outlier detection using IQR method on physical measurements
outlier_report = {}
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    mask = (df[col] < lower) | (df[col] > upper)
    outlier_report[col] = {
        'lower_bound': round(lower, 2),
        'upper_bound': round(upper, 2),
        'n_outliers': int(mask.sum()),
        'outlier_values': df.loc[mask, col].tolist()
    }

print("=== ROWS DROPPED (missing all measurements) ===", before_rows - after_rows)
print("\n=== OUTLIER REPORT (IQR method) ===")
for k, v in outlier_report.items():
    print(k, v)

# Step 7: Parse Date Egg into proper datetime
df['Date Egg'] = pd.to_datetime(df['Date Egg'], errors='coerce')
print("\nDate parse failures:", df['Date Egg'].isna().sum())

# ---------- SCREENSHOT 3: Missing values after cleaning ----------
plt.figure(figsize=(10, 5))
sns.heatmap(df.isna(), cbar=False, cmap='Greens', yticklabels=False)
plt.title('Missing Values After Cleaning')
plt.tight_layout()
plt.savefig('shot3_missing_after.png')
plt.close()

# ---------- SCREENSHOT 4: Distribution comparison ----------
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.flat, numeric_cols):
    sns.histplot(df[col], kde=True, ax=ax, color='seagreen')
    ax.set_title(f'{col} — Cleaned Distribution', fontsize=9)
plt.tight_layout()
plt.savefig('shot4_distributions_after.png')
plt.close()

# ---------- SCREENSHOT 5: Species count + sex balance ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
df['Species'].value_counts().plot(kind='bar', ax=axes[0], color='coral')
axes[0].set_title('Species Count')
axes[0].tick_params(axis='x', rotation=20)
df['Sex'].value_counts().plot(kind='bar', ax=axes[1], color='slateblue')
axes[1].set_title('Sex Distribution (after fillna)')
plt.tight_layout()
plt.savefig('shot5_species_sex.png')
plt.close()

df.to_csv('penguins_cleaned.csv', index=False)
print("\nFinal shape:", df.shape)
print("Saved penguins_cleaned.csv")
