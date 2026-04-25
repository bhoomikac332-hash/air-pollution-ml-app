import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

# Features: [PM2.5, Temperature, Age]
X = np.array([
    [20, 25, 18],
    [40, 28, 25],
    [60, 30, 35],
    [80, 35, 45],
    [100, 38, 55],
    [120, 40, 60],
    [150, 42, 70]
])

# Labels: 0=Low, 1=Medium, 2=High
y = np.array([0, 0, 1, 1, 2, 2, 2])

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model created!")