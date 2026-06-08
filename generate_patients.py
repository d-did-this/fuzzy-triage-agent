import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Total patients
N = 300
N_normal = int(N * 0.8) # 240
N_anom = N - N_normal   # 60

# Helper function to generate normal data within range
def gen_norm(loc, scale, size, min_val, max_val, is_int=False):
    vals = np.random.normal(loc, scale, size)
    vals = np.clip(vals, min_val, max_val)
    if is_int:
        return np.round(vals).astype(int)
    return np.round(vals, 1)

# --- NORMAL GROUP (N=240) ---
age_norm = gen_norm(49, 15, N_normal, 18, 80, True)
cr_norm = gen_norm(88, 10, N_normal, 62, 115, True)

# Generate eGFR with negative correlation to Age and Cr
# Using a base formula to ensure strong correlation
egfr_raw_norm = 175 - 0.5 * age_norm - 0.5 * cr_norm + np.random.normal(0, 3, N_normal)
# Normal eGFR is >= 90, capped at 120
egfr_norm = np.clip(np.round(egfr_raw_norm), 90, 120).astype(int)

hb_norm = gen_norm(15.2, 0.8, N_normal, 13.0, 17.5)
wbc_norm = gen_norm(7.6, 1.3, N_normal, 4.0, 11.2)
plt_norm = gen_norm(275, 45, N_normal, 150, 400, True)
neu_norm = gen_norm(57.5, 6.0, N_normal, 40.0, 75.0)
mcv_norm = gen_norm(88, 3, N_normal, 80, 96, True)
rdw_norm = gen_norm(13.4, 0.6, N_normal, 12.0, 14.8)

df_norm = pd.DataFrame({
    'Age': age_norm, 'Hb': hb_norm, 'WBC': wbc_norm, 'PLT': plt_norm,
    'NEU_pct': neu_norm, 'MCV': mcv_norm, 'RDW': rdw_norm,
    'Creatinine': cr_norm, 'eGFR': egfr_norm
})

# --- ANOMALOUS GROUP (N=60) ---
n_inf = 20
n_ane = 20
n_ren = 20

# 1. Infection (High WBC -> High NEU_pct)
age_inf = gen_norm(49, 15, n_inf, 18, 80, True)
cr_inf = gen_norm(88, 10, n_inf, 62, 115, True)
egfr_inf = np.clip(np.round(175 - 0.5 * age_inf - 0.5 * cr_inf + np.random.normal(0, 3, n_inf)), 90, 120).astype(int)

hb_inf = gen_norm(15.2, 0.8, n_inf, 13.0, 17.5)
wbc_inf = np.round(np.random.normal(16.0, 2.0, n_inf), 1) # Spiked > 12.0
# Ensure WBC is strictly > 12.0
wbc_inf = np.maximum(wbc_inf, 12.1)
plt_inf = gen_norm(275, 45, n_inf, 150, 400, True)
neu_inf = np.round(np.random.normal(85.0, 4.0, n_inf), 1) # Spiked > 75.0
# Ensure NEU_pct > 75.0
neu_inf = np.maximum(neu_inf, 75.1)
neu_inf = np.minimum(neu_inf, 99.0)
mcv_inf = gen_norm(88, 3, n_inf, 80, 96, True)
rdw_inf = gen_norm(13.4, 0.6, n_inf, 12.0, 14.8)

df_inf = pd.DataFrame({
    'Age': age_inf, 'Hb': hb_inf, 'WBC': wbc_inf, 'PLT': plt_inf,
    'NEU_pct': neu_inf, 'MCV': mcv_inf, 'RDW': rdw_inf,
    'Creatinine': cr_inf, 'eGFR': egfr_inf
})

# 2. Anemia (Low Hb -> Low or High MCV)
age_ane = gen_norm(49, 15, n_ane, 18, 80, True)
cr_ane = gen_norm(88, 10, n_ane, 62, 115, True)
egfr_ane = np.clip(np.round(175 - 0.5 * age_ane - 0.5 * cr_ane + np.random.normal(0, 3, n_ane)), 90, 120).astype(int)

hb_ane = np.round(np.random.normal(9.5, 1.0, n_ane), 1) # Low < 12.0
hb_ane = np.minimum(hb_ane, 11.9)
wbc_ane = gen_norm(7.6, 1.3, n_ane, 4.0, 11.2)
plt_ane = gen_norm(275, 45, n_ane, 150, 400, True)
neu_ane = gen_norm(57.5, 6.0, n_ane, 40.0, 75.0)

mcv_ane_low = np.round(np.random.normal(70, 4.0, n_ane//2)).astype(int)
mcv_ane_low = np.minimum(mcv_ane_low, 79)
mcv_ane_high = np.round(np.random.normal(105, 4.0, n_ane - n_ane//2)).astype(int)
mcv_ane_high = np.maximum(mcv_ane_high, 97)
mcv_ane = np.concatenate([mcv_ane_low, mcv_ane_high])
np.random.shuffle(mcv_ane)

rdw_ane = np.round(np.random.normal(16.5, 1.5, n_ane), 1) # Often high in anemia
df_ane = pd.DataFrame({
    'Age': age_ane, 'Hb': hb_ane, 'WBC': wbc_ane, 'PLT': plt_ane,
    'NEU_pct': neu_ane, 'MCV': mcv_ane, 'RDW': rdw_ane,
    'Creatinine': cr_ane, 'eGFR': egfr_ane
})

# 3. Renal Decline (High Age, High Cr -> Low eGFR)
# To explicitly show correlation, we spread the values out
age_ren = gen_norm(70, 8, n_ren, 50, 80, True) # Older
cr_ren = np.round(np.random.normal(200, 40, n_ren)).astype(int)
cr_ren = np.maximum(cr_ren, 120)

# Use the same base formula to keep global correlation strong, but don't clip at 90
egfr_raw_ren = 175 - 0.5 * age_ren - 0.5 * cr_ren + np.random.normal(0, 3, n_ren)
egfr_ren = np.clip(np.round(egfr_raw_ren), 5, 89).astype(int) # Sick eGFR

hb_ren = np.round(np.random.normal(11.5, 1.0, n_ren), 1)
wbc_ren = gen_norm(7.6, 1.3, n_ren, 4.0, 11.2)
plt_ren = gen_norm(275, 45, n_ren, 150, 400, True)
neu_ren = gen_norm(57.5, 6.0, n_ren, 40.0, 75.0)
mcv_ren = gen_norm(88, 3, n_ren, 80, 96, True)
rdw_ren = gen_norm(13.4, 0.6, n_ren, 12.0, 14.8)

df_ren = pd.DataFrame({
    'Age': age_ren, 'Hb': hb_ren, 'WBC': wbc_ren, 'PLT': plt_ren,
    'NEU_pct': neu_ren, 'MCV': mcv_ren, 'RDW': rdw_ren,
    'Creatinine': cr_ren, 'eGFR': egfr_ren
})

# Combine all anomalous
df_anom = pd.concat([df_inf, df_ane, df_ren])

# Combine everything and shuffle
df = pd.concat([df_norm, df_anom]).sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv('synthetic_patients.csv', index=False)

# Validation outputs
print("=== Dataset Description ===")
print(df.describe())
print("\n=== Pearson Correlation Matrix (Age, eGFR, Creatinine) ===")
print(df[['Age', 'eGFR', 'Creatinine']].corr())
