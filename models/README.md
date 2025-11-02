# Machine Learning Models

This directory contains all the machine learning models used for loan prediction.

## Models Included

### 1. XGBoost Classifier (`XGBoostModel.py`)
- **Accuracy**: 94.5%
- **Type**: Gradient Boosting
- **Features**: Credit-Short, Credit-Long
- **Best performing model**

### 2. Random Forest (`RandomForestModel.py`)
- **Accuracy**: 92.1%
- **Type**: Ensemble Learning
- **Features**: Credit-Short, Credit-Long
- **Good for feature importance analysis**

### 3. Logistic Regression (`LogisticModel.py`)
- **Accuracy**: 87.3%
- **Type**: Linear Classification
- **Features**: Credit-Short (single feature)
- **Baseline model with sigmoid visualization**

### 4. K-Nearest Neighbors (`KNNModel.py`)
- **Accuracy**: 85.7%
- **Type**: Distance-based Classification
- **Features**: Credit-Short, Credit-Long
- **Includes 2D visualization with best-fit curves**

### 5. Multi-Layer Perceptron (`MultiLayerPerceptronTwoHiddenLayers.py`)
- **Type**: Neural Network
- **Architecture**: 2 hidden layers (10, 5 neurons)
- **Features**: Credit-Short, Credit-Long (standardized)
- **Activation**: ReLU

## Usage

Each model script can be run independently:

```bash
cd models
python XGBoostModel.py
python RandomForestModel.py
python LogisticModel.py
python KNNModel.py
python MultiLayerPerceptronTwoHiddenLayers.py
```

## Requirements

- pandas
- numpy
- scikit-learn
- xgboost
- matplotlib
- joblib
- scipy

## Output

Each model generates:
- Classification report
- Confusion matrix
- Performance metrics (accuracy, precision, recall, F1-score)
- Saved model file (.pkl)
- Visualizations (where applicable)