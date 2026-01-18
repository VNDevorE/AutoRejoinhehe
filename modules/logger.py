"""
Logger Module
Handles logging with colors and file output
"""

import os
import logging
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredLogger:
    """Custom logger with colored output"""
    
    def __init__(self, name: str = "AutoRejoin", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup file logger
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        
        self.file_logger = logging.getLogger(name)
        self.file_logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        
        self.file_logger.addHandler(fh)
        
        # Stats
        self.stats = {
            'rejoin_attempts': 0,
            'rejoin_success': 0,
            'rejoin_failed': 0,
            'start_time': datetime.now()
        }
    
    def _log_to_file(self, level: str, message: str):
        """Log to file"""
        if level == "DEBUG":
            self.file_logger.debug(message)
        elif level == "INFO":
            self.file_logger.info(message)
        elif level == "WARNING":
            self.file_logger.warning(message)
        elif level == "ERROR":
            self.file_logger.error(message)
        elif level == "CRITICAL":
            self.file_logger.critical(message)
    
    def debug(self, message: str):
        """Debug message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.CYAN}[{timestamp}] [DEBUG] {message}{Style.RESET_ALL}")
        self._log_to_file("DEBUG", message)
    
    def info(self, message: str):
        """Info message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.GREEN}[{timestamp}] [INFO] {message}{Style.RESET_ALL}")
        self._log_to_file("INFO", message)
    
    def warning(self, message: str):
        """Warning message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.YELLOW}[{timestamp}] [WARNING] {message}{Style.RESET_ALL}")
        self._log_to_file("WARNING", message)
    
    def error(self, message: str):
        """Error message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.RED}[{timestamp}] [ERROR] {message}{Style.RESET_ALL}")
        self._log_to_file("ERROR", message)
    
    def critical(self, message: str):
        """Critical message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.WHITE}{Back.RED}[{timestamp}] [CRITICAL] {message}{Style.RESET_ALL}")
        self._log_to_file("CRITICAL", message)
    
    def success(self, message: str):
        """Success message (custom)"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Fore.GREEN}{Style.BRIGHT}[{timestamp}] [SUCCESS] ✓ {message}{Style.RESET_ALL}")
        self._log_to_file("INFO", f"SUCCESS: {message}")
    
    def banner(self, message: str):
        """Print banner"""
        border = "=" * 60
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{border}")
        print(f"{message.center(60)}")
        print(f"{border}{Style.RESET_ALL}\n")
        self._log_to_file("INFO", f"BANNER: {message}")
    
    def status(self, message: str):
        """Status update (no timestamp)"""
        print(f"{Fore.BLUE}► {message}{Style.RESET_ALL}")
    
    def increment_rejoin_attempt(self):
        """Increment rejoin attempt counter"""
        self.stats['rejoin_attempts'] += 1
    
    def increment_rejoin_success(self):
        """Increment rejoin success counter"""
        self.stats['rejoin_success'] += 1
    
    def increment_rejoin_failed(self):
        """Increment rejoin failed counter"""
        self.stats['rejoin_failed'] += 1
    
    def print_stats(self):
        """Print statistics"""
        uptime = datetime.now() - self.stats['start_time']
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        print(f"\n{Fore.CYAN}{'─' * 60}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}📊 STATISTICS")
        print(f"{Fore.CYAN}{'─' * 60}")
        print(f"{Fore.WHITE}Uptime:          {Fore.GREEN}{hours}h {minutes}m")
        print(f"{Fore.WHITE}Rejoin Attempts: {Fore.YELLOW}{self.stats['rejoin_attempts']}")
        print(f"{Fore.WHITE}Success:         {Fore.GREEN}{self.stats['rejoin_success']}")
        print(f"{Fore.WHITE}Failed:          {Fore.RED}{self.stats['rejoin_failed']}")
        
        if self.stats['rejoin_attempts'] > 0:
            success_rate = (self.stats['rejoin_success'] / self.stats['rejoin_attempts']) * 100
            print(f"{Fore.WHITE}Success Rate:    {Fore.CYAN}{success_rate:.1f}%")
        
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}\n")
