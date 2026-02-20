import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Create synthetic training data
np.random.seed(42)

data_size = 5000

credential_reuse = np.random.rand(data_size)
phishing_risk = np.random.rand(data_size)
public_exposure = np.random.rand(data_size)

# Target risk score (weighted)
risk = (
    0.5 * credential_reuse +
    0.3 * phishing_risk +
    0.2 * public_exposure
)

risk = np.clip(risk, 0, 1)

X = np.column_stack([
    credential_reuse,
    phishing_risk,
    public_exposure
])

y = (risk > 0.5).astype(int)

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "risk_model.pkl")

print("Model trained and saved successfully.")