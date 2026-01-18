#!/usr/bin/env python3
"""
Roblox AutoRejoin Tool
Automatically rejoins Roblox game when disconnected or crashed
"""

import os
import sys
import json
import signal
from modules import ColoredLogger, RobloxMonitor


def load_config(config_path: str = "config.json") -> dict:
    """
    Load configuration from JSON file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        sys.exit(1)


def print_banner():
    """Print welcome banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🎮  ROBLOX AUTO-REJOIN TOOL  🎮                   ║
║                                                           ║
║        Tự động vào lại game khi bị disconnect            ║
║        Chạy 24/7 trên Cloud Phone                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point"""
    # Print banner
    print_banner()
    
    # Load configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    print(f"✓ Game ID: {config['game_id']}")
    print(f"✓ Check Interval: {config['check_interval']}s")
    print(f"✓ Max Retries: {config['max_retries']}")
    print()
    
    # Initialize logger
    logger = ColoredLogger("AutoRejoin")
    
    # Initialize monitor
    monitor = RobloxMonitor(config, logger)
    
    # Setup signal handler for graceful shutdown
    def signal_handler(sig, frame):
        logger.warning("\n⚠️  Received shutdown signal")
        monitor.stop_monitoring()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start monitoring
    try:
        monitor.start_monitoring()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
