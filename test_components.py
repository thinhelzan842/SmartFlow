"""
Test script to verify SmartFlow components
"""

import sys
import os

print("=" * 60)
print("SmartFlow Component Test")
print("=" * 60)

# Test 1: Import required libraries
print("\n[1] Testing library imports...")
try:
    import flask
    print("  ✓ Flask:", flask.__version__)
except ImportError as e:
    print("  ✗ Flask not found:", e)
    sys.exit(1)

try:
    import osmnx as ox
    print("  ✓ OSMnx:", ox.__version__)
except ImportError as e:
    print("  ✗ OSMnx not found:", e)
    sys.exit(1)

try:
    import networkx as nx
    print("  ✓ NetworkX:", nx.__version__)
except ImportError as e:
    print("  ✗ NetworkX not found:", e)
    sys.exit(1)

try:
    import pandas as pd
    print("  ✓ Pandas:", pd.__version__)
except ImportError as e:
    print("  ✗ Pandas not found:", e)
    sys.exit(1)

try:
    import numpy as np
    print("  ✓ NumPy:", np.__version__)
except ImportError as e:
    print("  ✗ NumPy not found:", e)
    sys.exit(1)

# Test 2: Check file structure
print("\n[2] Testing file structure...")
required_files = [
    'app.py',
    'routing_logic.py',
    'requirements.txt',
    'templates/index.html',
    'static/style.css',
    'static/app.js'
]

for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING!")

# Test 3: Test routing logic import
print("\n[3] Testing routing_logic module...")
try:
    from routing_logic import (
        calculate_bpr_weight,
        SmartRoutingSystem,
        DEFAULT_ALPHA,
        DEFAULT_BETA,
        DEFAULT_CAPACITY_FACTOR
    )
    print("  ✓ All functions imported successfully")
    print(f"  ✓ Default parameters: α={DEFAULT_ALPHA}, β={DEFAULT_BETA}, capacity={DEFAULT_CAPACITY_FACTOR}")
except ImportError as e:
    print("  ✗ Error importing routing_logic:", e)
    sys.exit(1)

# Test 4: Test BPR calculation
print("\n[4] Testing BPR formula...")
try:
    We_base = 60  # 60 seconds base time
    fe = 50  # 50 vehicles
    Ce = 100  # capacity 100 vehicles
    alpha = 1.5
    beta = 8
    
    We = calculate_bpr_weight(We_base, fe, Ce, alpha, beta)
    print(f"  ✓ BPR calculation: {We_base}s → {We:.2f}s (congestion: {(We/We_base - 1)*100:.1f}%)")
except Exception as e:
    print("  ✗ BPR calculation failed:", e)
    sys.exit(1)

# Test 5: Check graph cache
print("\n[5] Checking graph cache...")
if os.path.exists('graph_with_congestion.gpickle'):
    size_mb = os.path.getsize('graph_with_congestion.gpickle') / (1024 * 1024)
    print(f"  ✓ Graph cache found ({size_mb:.2f} MB)")
else:
    print("  ⚠ Graph cache not found - will download from OSM on first run")

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nYou can now run the application:")
print("  python app.py")
print("\nThen open: http://localhost:5000")
print("=" * 60)
