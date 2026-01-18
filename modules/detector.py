"""
Detector Module
Detects various states of Roblox app
"""

import time
from typing import List, Optional
from .adb_helper import ADBHelper
from .logger import ColoredLogger


class RobloxDetector:
    """Detects Roblox app states"""
    
    # Common disconnect/error messages
    DISCONNECT_KEYWORDS = [
        "Disconnected",
        "Lost Connection",
        "Connection Lost",
        "Unable to Connect",
        "Error",
        "Kicked",
        "Please check your internet",
        "Reconnect"
    ]
    
    # In-game indicators
    INGAME_KEYWORDS = [
        "Chat",
        "Leaderboard",
        "Settings",
        "Menu"
    ]
    
    def __init__(self, adb: ADBHelper, logger: ColoredLogger, package_name: str):
        self.adb = adb
        self.logger = logger
        self.package_name = package_name
    
    def is_roblox_running(self) -> bool:
        """
        Check if Roblox is running
        
        Returns:
            True if Roblox process exists
        """
        return self.adb.is_package_running(self.package_name)
    
    def is_roblox_foreground(self) -> bool:
        """
        Check if Roblox is in foreground
        
        Returns:
            True if Roblox is the current activity
        """
        current_activity = self.adb.get_current_activity()
        
        if current_activity:
            return self.package_name in current_activity
        
        return False
    
    def is_disconnected(self) -> bool:
        """
        Check if showing disconnect message
        
        Returns:
            True if disconnect detected
        """
        if not self.is_roblox_running():
            self.logger.debug("Roblox not running - considered disconnected")
            return True
        
        # Get screen text
        screen_texts = self.adb.get_screen_text()
        
        # Check for disconnect keywords
        for text in screen_texts:
            for keyword in self.DISCONNECT_KEYWORDS:
                if keyword.lower() in text.lower():
                    self.logger.warning(f"Disconnect detected: '{text}'")
                    return True
        
        return False
    
    def is_in_game(self) -> bool:
        """
        Check if currently in game
        
        Returns:
            True if in game
        """
        if not self.is_roblox_running():
            return False
        
        # Get screen text
        screen_texts = self.adb.get_screen_text()
        
        # Simple heuristic: if we see game UI elements
        for text in screen_texts:
            for keyword in self.INGAME_KEYWORDS:
                if keyword.lower() in text.lower():
                    return True
        
        return False
    
    def is_on_home_screen(self) -> bool:
        """
        Check if on Android home screen
        
        Returns:
            True if on home screen
        """
        current_activity = self.adb.get_current_activity()
        
        if current_activity:
            # Common launcher activities
            home_indicators = [
                "launcher",
                "home",
                "desktop"
            ]
            
            for indicator in home_indicators:
                if indicator in current_activity.lower():
                    return True
        
        return False
    
    def detect_state(self) -> str:
        """
        Detect current state
        
        Returns:
            State string: 'not_running', 'disconnected', 'in_game', 'loading', 'unknown'
        """
        # Check if running
        if not self.is_roblox_running():
            return 'not_running'
        
        # Check if disconnected
        if self.is_disconnected():
            return 'disconnected'
        
        # Check if in game
        if self.is_in_game():
            return 'in_game'
        
        # Check if on home screen
        if self.is_on_home_screen():
            return 'not_running'
        
        # Probably loading or in menu
        return 'loading'
    
    def wait_for_state(self, target_state: str, timeout: int = 30, check_interval: int = 2) -> bool:
        """
        Wait for a specific state
        
        Args:
            target_state: State to wait for
            timeout: Maximum wait time in seconds
            check_interval: Check interval in seconds
            
        Returns:
            True if state reached
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_state = self.detect_state()
            
            if current_state == target_state:
                return True
            
            time.sleep(check_interval)
        
        return False
