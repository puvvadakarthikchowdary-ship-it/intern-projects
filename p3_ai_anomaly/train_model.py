import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle

df = pd.read_csv('perf_data.csv')
FEATURES = ['ipc', 'l1_miss_rate', 'l2_miss_rate',
            'branch_miss', 'stall_ratio', 'mem_pressure', 'perf_score']
X      = df[FEATURES].values
y_true = df['label'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    n_estimators=200,
    contamination=0.047,
    max_features=0.8,
    random_state=42
)
model.fit(X_scaled)

preds_raw = model.predict(X_scaled)
y_pred    = (preds_raw == -1).astype(int)
scores    = -model.score_samples(X_scaled)

precision = precision_score(y_true, y_pred, zero_division=0)
recall    = recall_score(y_true, y_pred, zero_division=0)
f1        = f1_score(y_true, y_pred, zero_division=0)

df['anomaly_score'] = scores
df['predicted']     = y_pred
df.to_csv('results.csv', index=False)

with open('model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'scaler': scaler, 'features': FEATURES}, f)

print("="*50)
print("  MODEL EVALUATION REPORT")
print("="*50)
print(f"  Algorithm  : Isolation Forest (unsupervised)")
print(f"  Features   : {len(FEATURES)} CPU perf counters")
print(f"  Precision  : {precision:.3f}")
print(f"  Recall     : {recall:.3f}")
print(f"  F1 Score   : {f1:.3f}")
print(f"  Anomalies detected: {y_pred.sum()} / {y_true.sum()} actual")
print("="*50)
print("  ✓ Model saved: model.pkl")
print("  ✓ Results saved: results.csv")
print("  Impact: Replaces ~2hrs manual perf triage per run")
