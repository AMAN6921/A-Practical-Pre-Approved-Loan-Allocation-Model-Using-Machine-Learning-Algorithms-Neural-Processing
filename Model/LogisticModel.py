import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load dataset
data = pd.read_excel("../FINAL_DATASET_ARRANGED_MP2024.xlsx")

X = data[['Credit-Short']].values  # single feature for sigmoid curve
y = data['Cust_Type'].values       # string labels: Very_Bad, Normal, Very_Good

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "LogisticModel.pkl")

# Predictions
y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Create sigmoid-like curve for probability of Very_Good
x_values = np.linspace(X.min() - 1, X.max() + 1, 300).reshape(-1, 1)
y_prob = model.predict_proba(x_values)[:, list(model.classes_).index("Very_Good")]

plt.plot(x_values, y_prob, color='black', linewidth=2, label="Sigmoid Curve (Very_Good)")

# Map colors for training data
color_map = {"Very_Bad": "red", "Normal": "yellow", "Very_Good": "green"}

for class_val in np.unique(y_train):
    idx = (y_train == class_val)
    plt.scatter(
        X_train[idx], model.predict_proba(X_train[idx])[:, list(model.classes_).index("Very_Good")],
        color=color_map[class_val], edgecolor='k', s=70, label=f"Train {class_val}"
    )

# Test data in blue
plt.scatter(
    X_test, model.predict_proba(X_test)[:, list(model.classes_).index("Very_Good")],
    color="blue", marker="x", s=80, label="Test Cases"
)

plt.xlabel("Credit-Short")
plt.ylabel("Probability of Very_Good")
plt.title("Logistic Regression - Sigmoid Curve with Classification")
plt.legend()
plt.show()