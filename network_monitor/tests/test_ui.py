import pytest
import time
import gc
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from network_monitor.ui.main_window import MainWindow
from network_monitor.ui.sound_manager import SoundManager
from network_monitor.ui.animation_manager import AnimationManager
from network_monitor.core.network_monitor import NetworkMonitor
from network_monitor.core.backup_manager import BackupManager
from network_monitor.core.security_manager import SecurityManager

# Define test timeouts
pytestmark = pytest.mark.timeout(10)  # Default 10 second timeout for all tests

@pytest.fixture(scope="function")
def app():
    """Create Qt application for testing in offscreen mode"""
    import os
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication([])
    yield app
    app.quit()
    # Force cleanup
    gc.collect()

@pytest.fixture
def security_manager():
    """Create security manager for testing"""
    from network_monitor.core.security_manager import SecurityManager
    return SecurityManager()

@pytest.fixture
def main_window(app, security_manager):
    """Create main window for testing"""
    window = MainWindow(security_manager)
    yield window
    # Cleanup after test
    if hasattr(window, 'close'):
        window.close()
    if hasattr(window, 'deleteLater'):
        window.deleteLater()
    app.processEvents()

def test_sound_notifications():
    """Test sound notifications for critical events"""
    sound_manager = SoundManager()
    
    # Test device offline sound
    start_time = time.time()
    sound_manager.play_sound('device_offline')
    sound_time = time.time() - start_time
    assert sound_time < 0.1, "Sound playback should not block"
    
    # Test network storm sound
    start_time = time.time()
    sound_manager.play_sound('network_storm')
    sound_time = time.time() - start_time
    assert sound_time < 0.1, "Sound playback should not block"
    
    # Test alert sound
    start_time = time.time()
    sound_manager.play_sound('alert')
    sound_time = time.time() - start_time
    assert sound_time < 0.1, "Sound playback should not block"

def test_animation_performance(app):
    """Test animation performance impact"""
    animation_manager = AnimationManager()
    test_widget = QWidget()
    
    # Test fade in animation
    start_time = time.time()
    animation_manager.fade_in(test_widget)
    animation_start_time = time.time() - start_time
    assert animation_start_time < 0.05, "Animation start should be near-instant"
    
    # Test flash status animation
    start_time = time.time()
    animation_manager.flash_status(test_widget, QColor(Qt.GlobalColor.red))
    animation_start_time = time.time() - start_time
    assert animation_start_time < 0.05, "Animation start should be near-instant"
    
    # Test multiple concurrent animations
    widgets = [QWidget() for _ in range(5)]
    start_time = time.time()
    for widget in widgets:
        animation_manager.fade_in(widget)
        animation_manager.flash_status(widget, QColor(Qt.GlobalColor.red))
    total_time = time.time() - start_time
    assert total_time < 0.1, "Multiple animations should not cause significant delay"
    
    # Test animation during IP status updates
    status_widget = QWidget()
    start_time = time.time()
    for _ in range(10):  # Simulate rapid status changes
        animation_manager.flash_status(status_widget, QColor(Qt.GlobalColor.green))
        animation_manager.flash_status(status_widget, QColor(Qt.GlobalColor.red))
    update_time = time.time() - start_time
    assert update_time < 0.2, "Status animations should not impact update speed"

@pytest.mark.timeout(3)
def test_program_controls():
    """Test program control buttons and configuration"""
    from network_monitor.core.network_monitor import NetworkMonitor
    
    # Initialize NetworkMonitor in test mode
    monitor = NetworkMonitor(test_mode=True)
    
    # Test default settings for test mode
    assert monitor.discovery_interval == 5, "Test mode scan interval should be 5 seconds"
    assert monitor.discovery_start_ip == '10.246.65.1', "Default start IP incorrect"
    assert monitor.discovery_end_ip == '10.246.81.254', "Default end IP incorrect"
    assert monitor._auto_save_interval == 20, "Test mode auto-save interval should be 20 seconds"
    
    # Test production mode settings
    prod_monitor = NetworkMonitor(test_mode=False)
    assert prod_monitor.discovery_interval == 300, "Production scan interval should be 5 minutes"
    assert prod_monitor._auto_save_interval == 1200, "Production auto-save interval should be 20 minutes"
    
    # Test scan range configuration
    monitor.set_discovery_range('192.168.1.1', '192.168.1.254')
    assert monitor.discovery_start_ip == '192.168.1.1', "Failed to update start IP"
    assert monitor.discovery_end_ip == '192.168.1.254', "Failed to update end IP"
    
    # Test scan interval configuration
    monitor.set_discovery_interval(600)  # 10 minutes
    assert monitor.discovery_interval == 600, "Failed to update scan interval"
    
    # Test auto-save configuration
    monitor.set_auto_save_interval(1800)  # 30 minutes
    assert monitor._auto_save_interval == 1800, "Failed to update auto-save interval"
    
    # Test invalid configurations
    with pytest.raises(ValueError):
        monitor.set_discovery_range('192.168.1.254', '192.168.1.1')  # Invalid range
    with pytest.raises(ValueError):
        monitor.set_discovery_interval(0)  # Invalid interval
    with pytest.raises(ValueError):
        monitor.set_auto_save_interval(-1)  # Invalid interval

@pytest.mark.timeout(5)
def test_auto_save():
    """Test auto-save functionality"""
    backup_manager = BackupManager()
    
    # Test auto-save interval (20 minutes)
    last_save = datetime.now() - timedelta(minutes=21)  # Past the 20-minute threshold
    backup_manager.last_save_time = last_save
    
    test_data = {"192.168.1.1": "Test Device"}
    should_save = backup_manager.should_save(test_data)
    assert should_save, "Should trigger save after 20 minutes"
    
    # Test no save needed before interval
    backup_manager.last_save_time = datetime.now() - timedelta(minutes=10)
    should_save = backup_manager.should_save(test_data)
    assert not should_save, "Should not save before 20-minute interval"
    
    # Test data integrity after save
    backup_manager.save_data(test_data, force=True)
    loaded_data = backup_manager.rollback()  # Use rollback to load latest backup
    assert loaded_data == test_data, "Data should be preserved after save and load"

if __name__ == "__main__":
    pytest.main(["-v", "test_ui.py"])
