#!/data/data/com.termux/files/usr/bin/bash

# Roblox AutoRejoin - Setup Script for Termux
# This script installs all required dependencies

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        🎮  ROBLOX AUTO-REJOIN SETUP  🎮                  ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Update package manager
echo "📦 Step 1: Updating package manager..."
pkg update -y
pkg upgrade -y

# Step 2: Install Python
echo "🐍 Step 2: Installing Python..."
pkg install python -y

# Step 3: Install pip
echo "📦 Step 3: Installing pip..."
pkg install python-pip -y

# Step 4: Install android-tools (for ADB)
echo "🔧 Step 4: Installing android-tools..."
pkg install android-tools -y

# Step 5: Install git (optional, for updates)
echo "📥 Step 5: Installing git..."
pkg install git -y

# Step 6: Install Python dependencies
echo "📚 Step 6: Installing Python packages..."
pip install --upgrade pip
pip install colorama

# Note: uiautomator2 and pure-python-adb might not work well in Termux
# We'll use direct ADB commands instead
echo "⚠️  Note: Using direct ADB commands (no uiautomator2 needed)"

# Step 7: Request storage permissions
echo "📁 Step 7: Requesting storage permissions..."
termux-setup-storage

# Step 8: Create necessary directories
echo "📂 Step 8: Creating directories..."
mkdir -p /sdcard/Download/AutoRejoin
mkdir -p /sdcard/Download/AutoRejoin/logs
mkdir -p /sdcard/Download/AutoRejoin/logs/screenshots

# Step 9: Copy files to Download folder (if running from different location)
echo "📋 Step 9: Setting up files..."
CURRENT_DIR=$(pwd)

if [ "$CURRENT_DIR" != "/sdcard/Download/AutoRejoin" ]; then
    echo "Copying files to /sdcard/Download/AutoRejoin..."
    cp -r * /sdcard/Download/AutoRejoin/
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Make sure you have ROOT access"
echo "   2. Run: su -c 'cd /sdcard/Download/AutoRejoin && python autorejoin.py'"
echo "   3. Or use the run.sh script"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - This tool requires ROOT access to work properly"
echo "   - Make sure Roblox is installed on your device"
echo "   - Configure config.json if needed"
echo ""
