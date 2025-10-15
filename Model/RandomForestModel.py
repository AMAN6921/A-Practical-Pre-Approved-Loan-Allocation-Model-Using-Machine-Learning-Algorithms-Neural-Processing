import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    mean_squared_error,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.preprocessing import LabelEncoder
from scipy import stats
import joblib

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_excel("../FINAL_DATASET_ARRANGED_MP2024.xlsx")

X = data[['Credit-Short', 'Credit-Long']].values
y = data['Cust_Type'].values  # categorical labels

# -----------------------------
# Encode categorical labels
# -----------------------------
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42
)

# -----------------------------
# Train Random Forest
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "RandomForestModel.pkl")

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Metrics
# -----------------------------
accuracy = accuracy_score(y_test, y_pred) * 100  # percentage
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
recall = recall_score(y_test, y_pred, average="macro", zero_division=0)
f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

# Z-scores of prediction errors
z_scores = stats.zscore(y_pred - y_test)

# -----------------------------
# Display metrics neatly
# -----------------------------
print("="*60)
print("Random Forest Classifier Performance Metrics")
print("="*60)
print(f"Accuracy           : {accuracy:.3f} %")
print(f"Model Mean Score   : {model.score(X_test, y_test)*100:.3f} %")
print(f"RMSE               : {rmse:.3f}")
print(f"Precision (Macro)  : {precision:.3f}")
print(f"Recall (Macro)     : {recall:.3f}")
print(f"F1 Score (Macro)   : {f1:.3f}")
print("="*60)
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_, digits=3))
print("="*60)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("="*60)
print("Z-Scores of Prediction Errors (first 10 shown):")
print(np.round(z_scores[:10], 3))
print("="*60)