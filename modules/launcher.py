"""
Launcher Module
Handles launching Roblox and joining games
"""

import time
import re
from typing import Optional
from urllib.parse import urlparse, parse_qs
from .adb_helper import ADBHelper
from .logger import ColoredLogger
from .detector import RobloxDetector


class RobloxLauncher:
    """Launches Roblox and joins games"""
    
    def __init__(self, adb: ADBHelper, logger: ColoredLogger, detector: RobloxDetector, 
                 package_name: str, game_id: str, vip_server_link: str = ""):
        self.adb = adb
        self.logger = logger
        self.detector = detector
        self.package_name = package_name
        self.game_id = game_id
        self.vip_server_link = vip_server_link
    
    def kill_roblox(self) -> bool:
        """
        Force stop Roblox
        
        Returns:
            True if successful
        """
        self.logger.debug("Killing Roblox process...")
        success = self.adb.force_stop_package(self.package_name)
        
        if success:
            self.logger.debug("Roblox killed successfully")
        else:
            self.logger.warning("Failed to kill Roblox")
        
        return success
    
    def launch_roblox(self) -> bool:
        """
        Launch Roblox app
        
        Returns:
            True if successful
        """
        self.logger.info("Launching Roblox...")
        
        # Try to start Roblox
        success = self.adb.start_activity(self.package_name)
        
        if success:
            self.logger.success("Roblox launched")
            time.sleep(3)  # Wait for app to initialize
            return True
        else:
            self.logger.error("Failed to launch Roblox")
            return False
    
    def _parse_vip_server_link(self, link: str) -> str:
        """
        Parse VIP server link and convert to Roblox deep link format
        
        Converts links like:
        - https://ro.blox.com/Ebh5?...&af_web_dp=https://www.roblox.com/share-links?code=XXX&type=Server
        - https://www.roblox.com/share-links?code=XXX&type=Server
        
        To:
        - roblox://navigation/share_links?code=XXX&type=Server
        
        Args:
            link: VIP server link (any format)
            
        Returns:
            Roblox deep link that the app can handle
        """
        try:
            server_code = None
            
            # Method 1: Extract from af_web_dp parameter (for ro.blox.com links)
            if 'ro.blox.com' in link or 'af_web_dp=' in link:
                self.logger.debug("Detected ro.blox.com link, extracting server code...")
                
                # Find af_web_dp parameter
                match = re.search(r'af_web_dp=([^&]+)', link)
                if match:
                    # URL decode the parameter
                    import urllib.parse
                    web_link = urllib.parse.unquote(match.group(1))
                    self.logger.debug(f"Extracted web link: {web_link}")
                    
                    # Extract code from the web link
                    code_match = re.search(r'code=([^&]+)', web_link)
                    if code_match:
                        server_code = code_match.group(1)
            
            # Method 2: Extract from deep_link_value parameter
            if not server_code and 'deep_link_value=' in link:
                match = re.search(r'code=([^&%]+)', link)
                if match:
                    server_code = match.group(1)
            
            # Method 3: Already in share-links or share format
            if not server_code and ('share-links' in link or '/share?' in link):
                self.logger.debug("Extracting from share link...")
                code_match = re.search(r'code=([^&]+)', link)
                if code_match:
                    server_code = code_match.group(1)
            
            # If we found a server code, convert to deep link
            if server_code:
                deep_link = f"roblox://navigation/share_links?code={server_code}&type=Server"
                self.logger.success(f"Converted to deep link: {deep_link}")
                return deep_link
            
            # Method 4: Already in roblox:// format
            if link.startswith('roblox://'):
                self.logger.debug("Link already in deep link format")
                return link
            
            # If all methods fail, return original link
            self.logger.warning(f"Could not parse VIP link, using original: {link}")
            return link
            
        except Exception as e:
            self.logger.error(f"Error parsing VIP link: {e}")
            return link

    
    def join_game_via_deeplink(self) -> bool:
        """
        Join game using deep link (most reliable method)
        Supports both regular game ID and VIP server links
        
        Returns:
            True if successful
        """
        # Check if VIP server link is provided
        if self.vip_server_link:
            self.logger.info(f"Joining VIP server via link...")
            # Parse and convert VIP link to direct format
            link_to_open = self._parse_vip_server_link(self.vip_server_link)
        else:
            self.logger.info(f"Joining game {self.game_id} via deep link...")
            link_to_open = f"roblox://placeId={self.game_id}"
        
        # Open link (works for both deep links and web links)
        # Force open with Roblox package to prevent opening in browser
        success = self.adb.open_url(link_to_open, package_name=self.package_name)
        
        if success:
            self.logger.success(f"Link opened: {link_to_open}")
            
            # Wait for game to load
            self.logger.status("Waiting for game to load...")
            time.sleep(10)  # Give time for game to load
            
            # Check if we need to click Play button
            self._handle_play_button()
            
            return True
        else:
            self.logger.error("Failed to open deep link")
            return False
    
    def _handle_play_button(self):
        """Handle clicking Play button if present"""
        # Get screen text
        screen_texts = self.adb.get_screen_text()
        
        # Look for Play button
        for text in screen_texts:
            if text.lower() in ['play', 'join', 'continue']:
                self.logger.debug(f"Found button: {text}")
                
                # Get screen size for tapping
                screen_size = self.adb.get_screen_size()
                
                if screen_size:
                    width, height = screen_size
                    
                    # Tap center of screen (where Play button usually is)
                    center_x = width // 2
                    center_y = int(height * 0.6)  # Slightly below center
                    
                    self.logger.debug(f"Tapping Play button at ({center_x}, {center_y})")
                    self.adb.tap(center_x, center_y)
                    time.sleep(2)
                
                break
    
    def launch_and_join(self, retry_count: int = 0, max_retries: int = 3) -> bool:
        """
        Complete launch and join sequence
        
        Args:
            retry_count: Current retry attempt
            max_retries: Maximum retry attempts
            
        Returns:
            True if successful
        """
        self.logger.info(f"Starting launch sequence (Attempt {retry_count + 1}/{max_retries + 1})...")
        
        try:
            # Step 1: Kill existing Roblox
            self.kill_roblox()
            time.sleep(2)
            
            # Step 2: Join via deep link (this will launch Roblox automatically)
            if not self.join_game_via_deeplink():
                raise Exception("Failed to join via deep link")
            
            # Step 3: Wait and verify
            self.logger.status("Verifying game join...")
            time.sleep(5)
            
            # Check if we're in game or loading
            state = self.detector.detect_state()
            
            if state in ['in_game', 'loading']:
                self.logger.success("Successfully joined game!")
                return True
            else:
                self.logger.warning(f"Unexpected state after join: {state}")
                
                # Retry if not at max
                if retry_count < max_retries:
                    self.logger.info(f"Retrying in 5 seconds...")
                    time.sleep(5)
                    return self.launch_and_join(retry_count + 1, max_retries)
                else:
                    return False
        
        except Exception as e:
            self.logger.error(f"Launch error: {e}")
            
            # Retry if not at max
            if retry_count < max_retries:
                self.logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
                return self.launch_and_join(retry_count + 1, max_retries)
            else:
                return False
    
    def rejoin_game(self) -> bool:
        """
        Rejoin game (wrapper for launch_and_join)
        
        Returns:
            True if successful
        """
        return self.launch_and_join()
