import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
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
import xgboost as xgb

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
    X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
)

# -----------------------------
# Train XGBoost Classifier
# -----------------------------
xgb_model = xgb.XGBClassifier(
    objective='multi:softprob',  # multi-class classification
    num_class=len(np.unique(y_encoded)),
    eval_metric='mlogloss',
    use_label_encoder=False,
    random_state=42
)

# Optional: Hyperparameter tuning with GridSearchCV
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [3, 5, 7],
#     'learning_rate': [0.01, 0.1, 0.2],
#     'subsample': [0.8, 1.0],
#     'colsample_bytree': [0.8, 1.0]
# }
# grid = GridSearchCV(xgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
# grid.fit(X_train, y_train)
# xgb_model = grid.best_estimator_

xgb_model.fit(X_train, y_train)

# Save model
joblib.dump(xgb_model, "XGBoostModel.pkl")

# -----------------------------
# Predictions
# -----------------------------
y_pred = xgb_model.predict(X_test)

# -----------------------------
# Metrics
# -----------------------------
accuracy = accuracy_score(y_test, y_pred) * 100
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
recall = recall_score(y_test, y_pred, average="macro", zero_division=0)
f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
z_scores = stats.zscore(y_pred - y_test)

# -----------------------------
# Display metrics neatly
# -----------------------------
print("="*60)
print("XGBoost Classifier Performance Metrics")
print("="*60)
print(f"Accuracy           : {accuracy:.3f} %")
print(f"Model Mean Score   : {xgb_model.score(X_test, y_test)*100:.3f} %")
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