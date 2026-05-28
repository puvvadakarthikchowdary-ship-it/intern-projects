import numpy as np
import pandas as pd

np.random.seed(42)
N_NORMAL  = 1000
N_ANOMALY = 50

normal = pd.DataFrame({
    'ipc':           np.random.normal(0.85, 0.08, N_NORMAL).clip(0.5, 1.0),
    'l1_miss_rate':  np.random.normal(0.05, 0.01, N_NORMAL).clip(0.01, 0.15),
    'l2_miss_rate':  np.random.normal(0.02, 0.005, N_NORMAL).clip(0.005, 0.08),
    'branch_miss':   np.random.normal(0.08, 0.02, N_NORMAL).clip(0.02, 0.2),
    'instructions':  (np.random.normal(5e8, 5e7, N_NORMAL)).astype(int),
    'label': 0
})

n_each = N_ANOMALY // 3

cache_anomaly = pd.DataFrame({
    'ipc':           np.random.normal(0.45, 0.05, n_each),
    'l1_miss_rate':  np.random.normal(0.35, 0.05, n_each),
    'l2_miss_rate':  np.random.normal(0.25, 0.04, n_each),
    'branch_miss':   np.random.normal(0.08, 0.02, n_each),
    'instructions':  (np.random.normal(3e8, 2e7, n_each)).astype(int),
    'label': 1
})

branch_anomaly = pd.DataFrame({
    'ipc':           np.random.normal(0.40, 0.06, n_each),
    'l1_miss_rate':  np.random.normal(0.06, 0.01, n_each),
    'l2_miss_rate':  np.random.normal(0.03, 0.005, n_each),
    'branch_miss':   np.random.normal(0.55, 0.06, n_each),
    'instructions':  (np.random.normal(4e8, 3e7, n_each)).astype(int),
    'label': 1
})

ipc_anomaly = pd.DataFrame({
    'ipc':           np.random.normal(0.20, 0.04, N_ANOMALY - 2*n_each),
    'l1_miss_rate':  np.random.normal(0.15, 0.03, N_ANOMALY - 2*n_each),
    'l2_miss_rate':  np.random.normal(0.12, 0.02, N_ANOMALY - 2*n_each),
    'branch_miss':   np.random.normal(0.20, 0.03, N_ANOMALY - 2*n_each),
    'instructions':  (np.random.normal(1e8, 1e7, N_ANOMALY - 2*n_each)).astype(int),
    'label': 1
})

def add_features(df):
    df['stall_ratio']  = (1.0 - df['ipc']).clip(0, 1)
    df['mem_pressure'] = df['l1_miss_rate'] * 4 + df['l2_miss_rate'] * 20
    df['perf_score']   = df['ipc'] / (df['mem_pressure'] + 0.01)
    return df

normal         = add_features(normal)
cache_anomaly  = add_features(cache_anomaly)
branch_anomaly = add_features(branch_anomaly)
ipc_anomaly    = add_features(ipc_anomaly)

df = pd.concat([normal, cache_anomaly, branch_anomaly, ipc_anomaly], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('perf_data.csv', index=False)

print(f"✓ Dataset saved: {len(df)} samples ({N_NORMAL} normal, {N_ANOMALY} anomalies)")
print("  Features: ipc, l1_miss_rate, l2_miss_rate, branch_miss, stall_ratio, mem_pressure, perf_score")
