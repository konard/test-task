#!/bin/bash
# Compilation and execution script for UnBasedCode.dpr

# Find FPC compiler (try common installation paths)
FPC=""
if command -v fpc >/dev/null 2>&1; then
    FPC="fpc"
elif [ -f "/c/tools/freepascal/bin/i386-win32/fpc.exe" ]; then
    FPC="/c/tools/freepascal/bin/i386-win32/fpc.exe"
elif [ -f "/c/FPC/3.2.2/bin/i386-win32/fpc.exe" ]; then
    FPC="/c/FPC/3.2.2/bin/i386-win32/fpc.exe"
elif [ -f "/c/FPC/3.2.2/bin/x86_64-win64/fpc.exe" ]; then
    FPC="/c/FPC/3.2.2/bin/x86_64-win64/fpc.exe"
else
    echo "Error: Free Pascal Compiler (fpc) not found"
    exit 1
fi

# Compile the program
$FPC UnBasedCode.dpr 2>&1

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
