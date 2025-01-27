import os
import time
import json
import gzip
from datetime import datetime
from typing import Dict, Optional, List
import logging
from functools import lru_cache

class BackupManager:
    """Manages auto-save and backup functionality for network monitor data"""
    
    def __init__(self, backup_dir: str = "backups", retention: int = 5):
        """
        Initialize the backup manager
        
        Args:
            backup_dir: Directory to store backups
            retention: Number of backups to retain
        """
        self.backup_dir = os.path.abspath(backup_dir)
        self.retention = retention
        self.last_data = None
        self.last_save_time = None
        os.makedirs(self.backup_dir, exist_ok=True)
        logging.info(f"初始化备份管理器，备份目录: {self.backup_dir}")
        
    def should_save(self, data: Dict, force: bool = False) -> bool:
        """
        Determine if data should be saved based on changes or time
        
        Args:
            data: Current data to compare
            force: Force save regardless of changes
        
        Returns:
            bool: True if save should occur
        """
        # Always save if forced or no previous save
        if force or self.last_save_time is None:
            return True
            
        # Check if 20 minutes have passed since last save
        if self.last_save_time:
            time_since_save = datetime.now() - self.last_save_time
            if time_since_save.total_seconds() >= 1200:  # 20 minutes
                # Only save if there are changes or exceptions
                return self._has_changes(data)
                
        return False
        
    def _has_changes(self, new_data: Dict) -> bool:
        """
        Check if new data has changes compared to last saved data
        
        Args:
            new_data: New data to compare
            
        Returns:
            bool: True if changes detected
        """
        if self.last_data is None:
            return True
            
        # Compare for changes or exceptions
        try:
            # Check for different keys
            if set(new_data.keys()) != set(self.last_data.keys()):
                return True
                
            # Check for changes in values
            for key in new_data:
                if new_data[key] != self.last_data[key]:
                    return True
                    
            return False
        except Exception:
            # If comparison fails, assume changes exist
            return True
    
    def save_data(self, data: Dict, force: bool = False) -> Optional[str]:
        """
        Save data to backup file if needed
        
        Args:
            data: Data to save
            force: Force save regardless of changes
            
        Returns:
            str: Path to backup file if saved, None otherwise
        """
        if not self.should_save(data, force):
            return None
            
        try:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            
            # Use gzip compression for backups
            compressed_filename = f"{filename}.gz"
            with gzip.open(compressed_filename, "wt", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
                
            self.last_data = data.copy()
            self.last_save_time = datetime.now()
            
            logging.info(f"数据已保存至: {filename}")
            self._rotate_backups()
            return filename
            
        except Exception as e:
            logging.error(f"保存备份时出错: {str(e)}")
            return None
    
    @lru_cache(maxsize=32)
    def list_backups(self) -> List[str]:
        """
        List available backup files
        
        Returns:
            List[str]: List of backup filenames
        """
        if not os.path.exists(self.backup_dir):
            return []
            
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.startswith("backup_") and (
                filename.endswith(".json.gz") or filename.endswith(".json")
            ):
                backups.append(filename)
        return sorted(backups, reverse=True)
    
    def rollback(self, backup_file: Optional[str] = None) -> Optional[Dict]:
        """
        Restore data from a backup file
        
        Args:
            backup_file: Specific backup file to restore, or None for latest
            
        Returns:
            Dict: Restored data if successful, None otherwise
        """
        try:
            if backup_file is None:
                backups = self.list_backups()
                if not backups:
                    logging.warning("没有可用的备份文件")
                    return None
                backup_file = os.path.join(self.backup_dir, backups[0])
            
            if not os.path.exists(backup_file):
                logging.error(f"备份文件不存在: {backup_file}")
                return None
                
            # Handle both compressed and uncompressed backups
            try:
                if backup_file.endswith('.gz'):
                    with gzip.open(backup_file, "rt", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    with open(backup_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
            except Exception as e:
                logging.error(f"读取备份文件时出错: {str(e)}")
                return None
                
            logging.info(f"已从文件恢复数据: {backup_file}")
            return data
            
        except Exception as e:
            logging.error(f"恢复备份时出错: {str(e)}")
            return None
    
    def _rotate_backups(self):
        """Remove old backups exceeding retention limit"""
        backups = self.list_backups()
        if len(backups) > self.retention:
            for old_backup in backups[self.retention:]:
                try:
                    os.remove(os.path.join(self.backup_dir, old_backup))
                    logging.info(f"已删除旧备份: {old_backup}")
                except Exception as e:
                    logging.error(f"删除旧备份时出错: {str(e)}")
