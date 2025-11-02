#!/usr/bin/env python3
"""
Simple startup script for Loan Prediction System
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 LOAN PREDICTION SYSTEM")
    print("=" * 30)
    
    # Check if this is first run
    if not Path("database/loan_prediction.db").exists():
        print("🔧 First time setup detected...")
        print("Running complete system setup...")
        subprocess.run([sys.executable, "scripts/setup_complete_system.py"])
    else:
        print("🚀 Starting system...")
        subprocess.run([sys.executable, "scripts/quick_start.py"])

if __name__ == "__main__":
    main()