#!/bin/bash
# Simple script to run the backend server

echo "🚀 Starting PALP AI - Backend Server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

# Check if models are trained
if [ ! -f "models/XGBoostModel.pkl" ]; then
    echo "⚠️  ML models not found. Training models..."
    echo ""
    cd models
    python XGBoostModel.py
    python RandomForestModel.py
    python LogisticModel.py
    python KNNModel.py
    python MultiLayerPerceptronTwoHiddenLayers.py
    cd ..
    echo ""
    echo "✅ Models trained successfully!"
    echo ""
fi

# Start the backend server
echo "🌐 Starting backend server on http://localhost:5000"
echo "💡 Press Ctrl+C to stop the server"
echo ""
python backend/app.py
