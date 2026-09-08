import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 120

df = pd.read_csv('penguins_cleaned.csv')
numeric_cols = ['Culmen Length (mm)', 'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)']

# Per-species IQR outlier detection (more meaningful than pooled IQR)
outlier_rows = []
for species, group in df.groupby('Species'):
    for col in numeric_cols:
        Q1, Q3 = group[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
        flagged = group[(group[col] < lower) | (group[col] > upper)]
        for idx, row in flagged.iterrows():
            outlier_rows.append({
                'Species': species, 'Column': col, 'Value': row[col],
                'Individual ID': row['Individual ID'],
                'Lower': round(lower,1), 'Upper': round(upper,1)
            })

outlier_df = pd.DataFrame(outlier_rows)
print("=== PER-SPECIES OUTLIERS FOUND ===")
print(outlier_df.to_string(index=False) if len(outlier_df) else "None found")
outlier_df.to_csv('per_species_outliers.csv', index=False)

# Screenshot: boxplots grouped by species (shows why pooled IQR was misleading)
fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))
for ax, col in zip(axes, numeric_cols):
    sns.boxplot(data=df, x='Species', y=col, ax=ax, palette='Set2')
    ax.set_title(col, fontsize=9)
    ax.tick_params(axis='x', rotation=25, labelsize=7)
    ax.set_xlabel('')
plt.tight_layout()
plt.savefig('shot6_boxplots_by_species.png')
plt.close()
print("\nSaved shot6_boxplots_by_species.png")
