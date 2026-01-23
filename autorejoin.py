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


def setup_game_config() -> dict:
    """
    Interactive setup for game configuration
    
    Returns:
        Game configuration dictionary
    """
    print("\n" + "="*60)
    print("🎮  THIẾT LẬP GAME")
    print("="*60)
    print()
    
    game_config = {}
    
    # Ask about VIP server
    while True:
        has_vip = input("❓ Bạn có VIP server không? (Y/N): ").strip().upper()
        
        if has_vip == 'Y':
            print("\n📋 Dán link VIP server vào đây:")
            print("   (Ví dụ: https://ro.blox.com/... hoặc https://www.roblox.com/share?code=...)")
            vip_link = input("👉 Link: ").strip()
            
            if vip_link:
                game_config['vip_server_link'] = vip_link
                game_config['game_id'] = ""  # Not needed when using VIP link
                print(f"\n✅ Đã lưu VIP server link!")
                break
            else:
                print("❌ Link không được để trống! Vui lòng thử lại.\n")
        
        elif has_vip == 'N':
            print("\n📋 Nhập Game ID:")
            print("   (Ví dụ: 1554960397)")
            game_id = input("👉 Game ID: ").strip()
            
            if game_id:
                game_config['game_id'] = game_id
                game_config['vip_server_link'] = ""
                print(f"\n✅ Đã lưu Game ID: {game_id}")
                break
            else:
                print("❌ Game ID không được để trống! Vui lòng thử lại.\n")
        
        else:
            print("❌ Vui lòng nhập Y hoặc N!\n")
    
    # Save to game_config.json
    try:
        with open('game_config.json', 'w', encoding='utf-8') as f:
            json.dump(game_config, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Đã lưu cấu hình vào game_config.json")
    except Exception as e:
        print(f"\n❌ Lỗi khi lưu config: {e}")
        sys.exit(1)
    
    print("="*60)
    print()
    
    return game_config


def load_game_config() -> dict:
    """
    Load game configuration from game_config.json
    If file doesn't exist, run interactive setup
    
    Returns:
        Game configuration dictionary
    """
    if os.path.exists('game_config.json'):
        try:
            with open('game_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️  game_config.json bị lỗi, chạy lại setup...\n")
            return setup_game_config()
    else:
        # First time setup
        return setup_game_config()


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
    
    # Load general configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    # Load or setup game configuration
    game_config = load_game_config()
    
    # Merge configs
    config.update(game_config)
    
    # Display configuration
    if config.get('vip_server_link'):
        print(f"✓ VIP Server: Đã cấu hình")
    else:
        print(f"✓ Game ID: {config.get('game_id', 'N/A')}")
    
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
