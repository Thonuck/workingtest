#!/usr/bin/env python
"""
Script to run pytest with coverage analysis for the users blueprint
"""
import sys
import subprocess

# Run pytest with coverage
result = subprocess.run([
    sys.executable, '-m', 'pytest',
    '--cov=app/blueprints/users',
    '--cov-report=term-missing',
    '-v'
], capture_output=False, text=True)

sys.exit(result.returncode)
