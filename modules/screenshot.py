"""
Screenshot Module
Handles taking screenshots for debugging
"""

import os
from datetime import datetime
from .adb_helper import ADBHelper
from .logger import ColoredLogger


class ScreenshotManager:
    """Manages screenshots for debugging"""
    
    def __init__(self, adb: ADBHelper, logger: ColoredLogger, screenshot_dir: str = "logs/screenshots"):
        self.adb = adb
        self.logger = logger
        self.screenshot_dir = screenshot_dir
        
        # Create screenshot directory
        os.makedirs(screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, prefix: str = "screen") -> str:
        """
        Take a screenshot
        
        Args:
            prefix: Filename prefix
            
        Returns:
            Path to saved screenshot or empty string if failed
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.logger.debug(f"Taking screenshot: {filename}")
        
        success = self.adb.take_screenshot(filepath)
        
        if success:
            self.logger.debug(f"Screenshot saved: {filepath}")
            return filepath
        else:
            self.logger.error("Failed to take screenshot")
            return ""
    
    def screenshot_on_error(self, error_type: str = "error"):
        """
        Take screenshot when error occurs
        
        Args:
            error_type: Type of error
        """
        self.take_screenshot(f"error_{error_type}")
