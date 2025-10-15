import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from numpy.polynomial.polynomial import Polynomial

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_excel("../FINAL_DATASET_ARRANGED_MP2024.xlsx")

X = data[['Credit-Short', 'Credit-Long']].values  # two features for 2D plot
y = data['Cust_Type'].values

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# -----------------------------
# Train KNN classifier
# -----------------------------
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

# Save model
joblib.dump(knn_model, "KNNModel.pkl")

# Predictions
y_pred = knn_model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------
# Scatter plot 2D with best-fit lines
# -----------------------------
plt.figure(figsize=(10,6))

# Training points
train_colors = {"Very_Bad": "red", "Normal": "yellow", "Very_Good": "green"}
for class_val in np.unique(y_train):
    idx = (y_train == class_val)
    plt.scatter(
        X_train[idx, 0], X_train[idx, 1],
        color=train_colors[class_val],
        edgecolor='k',
        s=70,
        label=f"Train {class_val}"
    )

# Test points colored by predicted class
test_colors = {"Very_Bad": "black", "Normal": "grey", "Very_Good": "blue"}
for class_val in np.unique(y_pred):
    idx = (y_pred == class_val)
    plt.scatter(
        X_test[idx, 0], X_test[idx, 1],
        color=test_colors[class_val],
        marker='x',
        s=100,
        label=f"Test Pred {class_val}"
    )

# -----------------------------
# Best-fit curves for each training class (using Polynomial fit)
# -----------------------------
for class_val in np.unique(y_train):
    idx = (y_train == class_val)
    x_class = X_train[idx, 0]
    y_class = X_train[idx, 1]
    if len(x_class) > 1:
        # Fit a 2nd-degree polynomial
        coefs = Polynomial.fit(x_class, y_class, 2).convert().coef
        x_fit = np.linspace(x_class.min(), x_class.max(), 300)
        y_fit = coefs[0] + coefs[1]*x_fit + coefs[2]*x_fit**2
        plt.plot(x_fit, y_fit, color=train_colors[class_val], linestyle='--', linewidth=2)

plt.xlabel("Credit-Short")
plt.ylabel("Credit-Long")
plt.title("KNN Classification: Training & Test Points with Best-Fit Curves")
plt.legend()
plt.show()