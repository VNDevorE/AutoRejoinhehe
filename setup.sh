#!/data/data/com.termux/files/usr/bin/bash

# Roblox AutoRejoin - Minimal Setup Script
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        🎮  ROBLOX AUTO-REJOIN MINIMAL SETUP  🎮          ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Step 1: Install Git & Python dependencies
echo "📦 Installing Git..."
pkg install git -y

echo "📚 Installing Python packages..."
pip install colorama

# Step 2: Create necessary directories
echo "📂 Creating log directories..."
mkdir -p logs/screenshots

# Step 3: Check for ROOT
echo "🔍 Checking for ROOT access..."
if [ "$(id -u)" -ne 0 ]; then
    echo "⚠️  Note: Root access not detected. Remember to run with 'su' later."
else
    echo "✅ Root access confirmed."
fi

echo ""
echo "✅ Setup completed!"
echo "🚀 Run tool: su -c 'python autorejoin.py'"
