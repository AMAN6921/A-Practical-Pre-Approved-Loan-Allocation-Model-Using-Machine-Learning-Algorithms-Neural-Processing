#!/bin/bash
# Start Full Loan Prediction System
echo "🚀 Starting Loan Prediction System..."

# Start backend in background
echo "📡 Starting API server..."
cd backend && python app.py &
BACKEND_PID=$!

# Start frontend
echo "🌐 Starting React frontend..."
cd ..
npm start &
FRONTEND_PID=$!

echo "✅ System started!"
echo "📡 API Server: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
