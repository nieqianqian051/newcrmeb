import pytest
import asyncio
from datetime import datetime, timedelta
from network_monitor.core.network_monitor import NetworkMonitor

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_discovery_intervals():
    """Test discovery interval configuration and scanning frequency"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Verify default intervals
    assert monitor.discovery_interval == 5, "Default interval should be 5 seconds in test mode"
    
    # Test production mode intervals
    prod_monitor = NetworkMonitor(test_mode=False)
    assert prod_monitor.discovery_interval == 300, "Production interval should be 300 seconds (5 minutes)"
    
    # Test interval modification
    monitor.set_discovery_interval(10)
    assert monitor.discovery_interval == 10, "Failed to update discovery interval"
    
    # Test scanning range
    assert monitor.discovery_start_ip == '10.246.65.1', "Incorrect default start IP"
    assert monitor.discovery_end_ip == '10.246.81.254', "Incorrect default end IP"

@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_auto_save():
    """Test auto-save functionality and intervals"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Verify auto-save interval
    assert monitor._auto_save_interval == 20, "Auto-save interval should be 20 seconds in test mode"
    
    # Test production mode
    prod_monitor = NetworkMonitor(test_mode=False)
    assert prod_monitor._auto_save_interval == 1200, "Production auto-save should be 1200 seconds (20 minutes)"
    
    # Test auto-save trigger
    initial_time = monitor.last_save_time
    monitor.last_save_time = datetime.now() - timedelta(seconds=21)  # Past the 20-second threshold
    
    # Add test data to trigger save
    monitor.add_ip('192.168.1.1', 'Test Device')
    monitor.save_data()
    
    assert monitor.last_save_time > initial_time, "Auto-save should update last_save_time"

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_scanning_range():
    """Test IP scanning range configuration"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Test default range
    assert monitor._discovery_start_ip == '10.246.65.1', "Incorrect default start IP"
    assert monitor._discovery_end_ip == '10.246.81.254', "Incorrect default end IP"
    
    # Test range modification
    monitor.set_discovery_range('192.168.1.1', '192.168.1.254')
    assert monitor._discovery_start_ip == '192.168.1.1', "Failed to update start IP"
    assert monitor._discovery_end_ip == '192.168.1.254', "Failed to update end IP"
    
    # Test invalid range
    with pytest.raises(ValueError):
        monitor.set_discovery_range('192.168.1.254', '192.168.1.1')

@pytest.mark.asyncio
@pytest.mark.timeout(15)
async def test_discovery_process():
    """Test actual discovery process with intervals"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Start discovery
    discovery_task = asyncio.create_task(monitor.start_discovery())
    
    # Let it run for a few intervals
    await asyncio.sleep(7)  # Should complete at least one scan
    
    # Stop discovery
    monitor.stop_discovery()
    await discovery_task
    
    # Verify discovered devices
    assert len(monitor.ip_data) > 0, "Should discover at least one device"

if __name__ == "__main__":
    pytest.main(["-v", "test_intervals.py"])
