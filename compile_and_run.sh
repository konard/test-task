#!/bin/bash
# Compilation and execution script for UnBasedCode.dpr

set -e

echo "=== Compiling UnBasedCode.dpr ==="
fpc -v UnBasedCode.dpr 2>&1 | tee compile.log

echo ""
echo "=== Compilation successful ==="
echo ""

if [ -f UnBasedCode ]; then
    echo "=== Executing UnBasedCode ==="
    ./UnBasedCode 2>&1 | tee execution.log || {
        EXIT_CODE=$?
        echo "Program exited with code: $EXIT_CODE"
        echo "Exit code: $EXIT_CODE" >> execution.log
    }
else
    echo "Error: Executable not found"
    exit 1
fi

echo ""
echo "=== Execution complete ==="
