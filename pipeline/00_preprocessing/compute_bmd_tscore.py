# BMD
import pandas as pd
import numpy as np
metadata = pd.read_csv('./SraRunTable.csv')
metadata.rename(columns={'Run': 'sample'}, inplace=True)
metadata = metadata[['sample','Fracture', 'HTOT_BMD_(g/cm2)', 'age', 'BMI']]

df = metadata.copy()

df.rename(columns={'HTOT_BMD_(g/cm2)': 'BMD_hip'}, inplace=True)

# References for Europoid women (60+, total hip)
REF_MEAN_HIP = 0.892   # g/cm²
REF_SD_HIP = 0.120

# T-score calculation
df['T_score'] = (df['BMD_hip'] - REF_MEAN_HIP) / REF_SD_HIP

# 0 = normal (T ≥ -1), 1 = osteopinia(osteoporosis) (T < -1)
df['BMD_group'] = (df['T_score'] < -1.0).astype(int)

# Categories
df['BMD_category'] = pd.cut(df['T_score'], 
                            bins=[-np.inf, -2.5, -1.0, np.inf],
                            labels=['Osteoporosis', 'Osteopenia', 'Normal'])
