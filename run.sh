#!/bin/bash
# Ultimate simple script - just run everything!

clear

cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🌾 PALP AI - PRE-APPROVED LOAN PREDICTION 🌾              ║
║                                                                              ║
║                         Starting the system...                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF

echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if models exist, if not train them
if [ ! -f "models/XGBoostModel.pkl" ]; then
    echo "📦 Training ML models (first time only)..."
    cd models
    python XGBoostModel.py > /dev/null 2>&1
    python RandomForestModel.py > /dev/null 2>&1
    python LogisticModel.py > /dev/null 2>&1
    python KNNModel.py > /dev/null 2>&1
    python MultiLayerPerceptronTwoHiddenLayers.py > /dev/null 2>&1
    cd ..
    echo "✅ Models trained!"
fi

# Start backend
echo "🚀 Starting backend server..."
python backend/app.py > /dev/null 2>&1 &
BACKEND_PID=$!

# Wait for server
sleep 3

# Check if server started
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ Backend running on http://localhost:5000"
    echo ""
    echo "🎨 Opening demo interface..."
    open frontend/index.html
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ SYSTEM IS RUNNING!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Backend API:  http://localhost:5000"
    echo "🎨 Demo UI:      Opened in your browser"
    echo "🏥 Health Check: http://localhost:5000/api/health"
    echo ""
    echo "💡 To stop the server: kill $BACKEND_PID"
    echo "   Or press Ctrl+C and run: kill $BACKEND_PID"
    echo ""
    
    # Keep script running
    trap "echo ''; echo '👋 Stopping server...'; kill $BACKEND_PID 2>/dev/null; exit" INT TERM
    wait $BACKEND_PID
else
    echo "❌ Failed to start server"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
