"""
Monitor Module
Main monitoring loop for AutoRejoin
"""

import time
from typing import Optional
from .adb_helper import ADBHelper
from .logger import ColoredLogger
from .detector import RobloxDetector
from .launcher import RobloxLauncher


class RobloxMonitor:
    """Monitors Roblox and handles auto-rejoin"""
    
    def __init__(self, config: dict, logger: ColoredLogger):
        self.config = config
        self.logger = logger
        
        # Initialize components
        self.adb = ADBHelper()
        self.detector = RobloxDetector(
            self.adb, 
            self.logger, 
            config['roblox_package']
        )
        self.launcher = RobloxLauncher(
            self.adb,
            self.logger,
            self.detector,
            config['roblox_package'],
            config['game_id'],
            config.get('vip_server_link', '')
        )
        
        # State tracking
        self.last_state = None
        self.consecutive_failures = 0
        self.is_running = False
    
    def check_and_rejoin(self) -> bool:
        """
        Check state and rejoin if needed
        
        Returns:
            True if action taken
        """
        # Detect current state
        state = self.detector.detect_state()
        
        # Log state change
        if state != self.last_state:
            self.logger.info(f"State changed: {self.last_state} → {state}")
            self.last_state = state
        
        # Handle states
        if state == 'not_running':
            self.logger.warning("⚠️  Roblox not running!")
            return self._handle_rejoin("Roblox crashed or closed")
        
        elif state == 'disconnected':
            self.logger.warning("⚠️  Disconnected from game!")
            return self._handle_rejoin("Disconnected")
        
        elif state == 'in_game':
            # All good, reset failure counter
            if self.consecutive_failures > 0:
                self.logger.success("Back in game, resetting failure counter")
                self.consecutive_failures = 0
            return False
        
        elif state == 'loading':
            self.logger.debug("Game is loading...")
            return False
        
        else:
            self.logger.debug(f"Unknown state: {state}")
            return False
    
    def _handle_rejoin(self, reason: str) -> bool:
        """
        Handle rejoin logic
        
        Args:
            reason: Reason for rejoin
            
        Returns:
            True if rejoin attempted
        """
        self.logger.increment_rejoin_attempt()
        self.logger.warning(f"🔄 Attempting to rejoin... (Reason: {reason})")
        
        # Attempt rejoin
        success = self.launcher.rejoin_game()
        
        if success:
            self.logger.increment_rejoin_success()
            self.logger.success("✓ Successfully rejoined!")
            self.consecutive_failures = 0
            return True
        else:
            self.logger.increment_rejoin_failed()
            self.logger.error("✗ Failed to rejoin")
            self.consecutive_failures += 1
            
            # Check if too many failures
            if self.consecutive_failures >= self.config['max_retries']:
                self.logger.critical(f"⚠️  Too many consecutive failures ({self.consecutive_failures})")
                self.logger.warning("Waiting 60 seconds before next attempt...")
                time.sleep(60)
                self.consecutive_failures = 0  # Reset after long wait
            
            return False
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        self.is_running = True
        
        self.logger.banner("🎮 ROBLOX AUTO-REJOIN STARTED 🎮")
        self.logger.info(f"Game ID: {self.config['game_id']}")
        self.logger.info(f"Check Interval: {self.config['check_interval']}s")
        self.logger.info(f"Max Retries: {self.config['max_retries']}")
        self.logger.info("")
        
        # Initial check - launch if not running
        initial_state = self.detector.detect_state()
        self.logger.info(f"Initial state: {initial_state}")
        
        if initial_state != 'in_game':
            self.logger.info("Starting initial game join...")
            self.launcher.rejoin_game()
        
        # Main monitoring loop
        try:
            iteration = 0
            
            while self.is_running:
                iteration += 1
                
                # Check and rejoin if needed
                self.check_and_rejoin()
                
                # Print stats every 20 iterations
                if iteration % 20 == 0:
                    self.logger.print_stats()
                
                # Wait before next check
                time.sleep(self.config['check_interval'])
        
        except KeyboardInterrupt:
            self.logger.warning("\n⚠️  Monitoring stopped by user")
            self.stop_monitoring()
        
        except Exception as e:
            self.logger.critical(f"Fatal error: {e}")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_running = False
        self.logger.banner("🛑 MONITORING STOPPED 🛑")
        self.logger.print_stats()
