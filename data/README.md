# Dataset Information

This directory contains the datasets used for training and testing the loan prediction models.

## Files

### `FINAL_DATASET_ARRANGED_MP2024.xlsx`
- **Purpose**: Training dataset for machine learning models
- **Features**: 
  - Credit-Short: Short-term credit score
  - Credit-Long: Long-term credit score
  - CPH: Credit Payment History
  - Payment History: Overall payment history
  - APH: Average Payment History
  - Time Limitations: Time-based constraints
  - Fluctuations: Credit fluctuation patterns
  - Employment: Employment status
  - Income: Income information
  - Other financial indicators
- **Target**: Cust_Type (Very_Bad, Normal, Very_Good)

### `TEST_CASES_ARRANGED_MP2024.xlsx`
- **Purpose**: Test cases for model validation
- **Structure**: Similar to training dataset
- **Usage**: Independent testing and validation

## Data Schema

| Column | Type | Description |
|--------|------|-------------|
| Credit-Short | Float | Short-term credit score (0-100) |
| Credit-Long | Float | Long-term credit score (0-100) |
| CPH | Float | Credit Payment History score |
| Payment History | Float | Overall payment history |
| APH | Float | Average Payment History |
| Time Limitations | Float | Time-based constraints |
| Fluctuations | Float | Credit fluctuation patterns |
| Employment | Float | Employment status indicator |
| Income | Float | Income level |
| Cust_Type | String | Target variable (Very_Bad/Normal/Very_Good) |

## Usage in Models

All models reference these datasets using relative paths:
```python
data = pd.read_excel("../data/FINAL_DATASET_ARRANGED_MP2024.xlsx")
```