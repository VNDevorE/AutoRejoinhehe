"""
ADB Helper Module
Wrapper for Android Debug Bridge commands
"""

import subprocess
import time
import re
from typing import Optional, List, Tuple


class ADBHelper:
    """Helper class for ADB operations"""
    
    def __init__(self):
        self.device_id = None
        self._check_adb_available()
    
    def _check_adb_available(self) -> bool:
        """Check if ADB is available"""
        try:
            result = self.shell_command("echo 'test'")
            return result is not None
        except Exception as e:
            raise RuntimeError(f"ADB not available: {e}")
    
    def shell_command(self, command: str, timeout: int = 10) -> Optional[str]:
        """
        Execute ADB shell command
        
        Args:
            command: Shell command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Command output or None if failed
        """
        try:
            # On Termux with root, we can directly execute shell commands
            full_command = command
            
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except subprocess.TimeoutExpired:
            print(f"Command timeout: {command}")
            return None
        except Exception as e:
            print(f"Command error: {e}")
            return None
    
    def is_package_running(self, package_name: str) -> bool:
        """
        Check if a package is currently running
        
        Args:
            package_name: Android package name
            
        Returns:
            True if package is running
        """
        output = self.shell_command(f"pidof {package_name}")
        return output is not None and len(output) > 0
    
    def get_current_activity(self) -> Optional[str]:
        """
        Get current foreground activity
        
        Returns:
            Current activity name or None
        """
        output = self.shell_command("dumpsys window windows | grep -E 'mCurrentFocus'")
        
        if output:
            # Extract activity name from output
            match = re.search(r'([a-zA-Z0-9.]+)/([a-zA-Z0-9.]+)', output)
            if match:
                return match.group(0)
        
        return None
    
    def force_stop_package(self, package_name: str) -> bool:
        """
        Force stop a package
        
        Args:
            package_name: Package to stop
            
        Returns:
            True if successful
        """
        output = self.shell_command(f"am force-stop {package_name}")
        time.sleep(1)
        return not self.is_package_running(package_name)
    
    def start_activity(self, package_name: str, activity_name: Optional[str] = None) -> bool:
        """
        Start an activity
        
        Args:
            package_name: Package name
            activity_name: Activity name (optional)
            
        Returns:
            True if successful
        """
        if activity_name:
            cmd = f"am start -n {package_name}/{activity_name}"
        else:
            cmd = f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        
        output = self.shell_command(cmd)
        time.sleep(2)
        return self.is_package_running(package_name)
    
    def open_url(self, url: str, package_name: Optional[str] = None) -> bool:
        """
        Open URL with intent
        
        Args:
            url: URL to open (e.g., roblox://placeId=123 or https://www.roblox.com/share?...)
            package_name: Optional package to force open with (e.g., com.roblox.client)
            
        Returns:
            True if successful
        """
        if package_name:
            # Force open with specific package (prevents opening in browser)
            cmd = f"am start -a android.intent.action.VIEW -d '{url}' -p {package_name}"
        else:
            # Let Android choose the app
            cmd = f"am start -a android.intent.action.VIEW -d '{url}'"
        
        output = self.shell_command(cmd)
        time.sleep(3)
        return output is not None
    
    def tap(self, x: int, y: int) -> bool:
        """
        Tap at coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        output = self.shell_command(f"input tap {x} {y}")
        time.sleep(0.5)
        return output is not None
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """
        Swipe from one point to another
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Swipe duration in ms
            
        Returns:
            True if successful
        """
        output = self.shell_command(f"input swipe {x1} {y1} {x2} {y2} {duration}")
        time.sleep(0.5)
        return output is not None
    
    def input_text(self, text: str) -> bool:
        """
        Input text
        
        Args:
            text: Text to input
            
        Returns:
            True if successful
        """
        # Escape special characters
        text = text.replace(' ', '%s')
        output = self.shell_command(f"input text '{text}'")
        time.sleep(0.5)
        return output is not None
    
    def press_key(self, keycode: int) -> bool:
        """
        Press a key
        
        Args:
            keycode: Android keycode (e.g., 4 for BACK)
            
        Returns:
            True if successful
        """
        output = self.shell_command(f"input keyevent {keycode}")
        time.sleep(0.5)
        return output is not None
    
    def get_screen_size(self) -> Optional[Tuple[int, int]]:
        """
        Get screen resolution
        
        Returns:
            (width, height) or None
        """
        output = self.shell_command("wm size")
        
        if output:
            match = re.search(r'(\d+)x(\d+)', output)
            if match:
                return (int(match.group(1)), int(match.group(2)))
        
        return None
    
    def take_screenshot(self, save_path: str) -> bool:
        """
        Take screenshot
        
        Args:
            save_path: Path to save screenshot
            
        Returns:
            True if successful
        """
        # Take screenshot to device
        device_path = "/sdcard/screenshot_temp.png"
        self.shell_command(f"screencap -p {device_path}")
        
        # Copy to destination
        try:
            subprocess.run(
                f"cp {device_path} {save_path}",
                shell=True,
                check=True
            )
            return True
        except:
            return False
    
    def get_screen_text(self) -> List[str]:
        """
        Get all text visible on screen using UI dump
        
        Returns:
            List of text strings
        """
        # Dump UI hierarchy
        output = self.shell_command("uiautomator dump /dev/tty")
        
        if not output:
            return []
        
        # Extract text attributes
        texts = re.findall(r'text="([^"]*)"', output)
        return [t for t in texts if t]  # Filter empty strings
