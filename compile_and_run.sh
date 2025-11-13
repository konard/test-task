#!/bin/bash
# Compilation and execution script for UnBasedCode.dpr

# Compile the program
fpc UnBasedCode.dpr 2>&1

echo ""

# Execute the compiled program (Windows: UnBasedCode.exe, Linux: UnBasedCode)
if [ -f UnBasedCode.exe ]; then
    ./UnBasedCode.exe 2>&1 || true
elif [ -f UnBasedCode ]; then
    ./UnBasedCode 2>&1 || true
else
    echo "Error: Executable not found"
    exit 1
fi
