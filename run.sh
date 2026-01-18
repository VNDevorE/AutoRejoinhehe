#!/data/data/com.termux/files/usr/bin/bash

# Roblox AutoRejoin - Run Script
# Runs the tool with proper environment and root privileges

echo "🚀 Starting Roblox AutoRejoin..."
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Not running as root. Attempting to run with su..."
    CURRENT_DIR=$(pwd)
    su -c "export PATH=\$PATH:/data/data/com.termux/files/usr/bin && \
           export TERM=xterm-256color && \
           cd $CURRENT_DIR && \
           python autorejoin.py"
else
    # Already root
    export PATH=$PATH:/data/data/com.termux/files/usr/bin
    export TERM=xterm-256color
    python autorejoin.py
fi
