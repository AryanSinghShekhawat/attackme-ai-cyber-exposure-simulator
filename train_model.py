import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Step 1: Generate synthetic data
data = []

for _ in range(10000):
    credential_reuse = np.random.uniform(0, 1)
    phishing_risk = np.random.uniform(0, 1)
    public_exposure = np.random.uniform(0, 1)

    # simulated ground truth risk
    risk = (
        0.4 * credential_reuse +
        0.3 * phishing_risk +
        0.3 * public_exposure
    )

    data.append([
        credential_reuse,
        phishing_risk,
        public_exposure,
        risk
    ])

df = pd.DataFrame(data, columns=[
    "credential_reuse",
    "phishing_risk",
    "public_exposure",
    "risk"
])

X = df.drop("risk", axis=1)
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, preds))

joblib.dump(model, "risk_model.pkl")