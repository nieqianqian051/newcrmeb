import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from datetime import datetime
from network_monitor.core.network_monitor import NetworkMonitor

@pytest.fixture
def mock_network():
    """Mock network operations for testing"""
    with patch('network_monitor.core.network_monitor.NetworkMonitor._cached_ping') as mock_ping:
        # Configure mock ping responses with different recovery behaviors
        attempt_count = {}
        def ping_response(ip):
            attempt_count[ip] = attempt_count.get(ip, 0) + 1
            # IP-specific behaviors
            if ip == "192.168.1.1" and attempt_count[ip] >= 2:  # First test IP recovers after 2 attempts
                return 50.0
            elif ip == "192.168.1.3" and attempt_count[ip] >= 2:  # First concurrent IP recovers after 2 attempts
                return 50.0
            elif ip in ["192.168.1.2", "192.168.1.4"]:  # These IPs never recover
                return None
            return None
        mock_ping.side_effect = ping_response
        yield mock_ping

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_connection_recovery(mock_network):
    """Test connection recovery mechanism"""
    monitor = None
    try:
        monitor = NetworkMonitor(test_mode=True)
        test_ip = "192.168.1.1"
        monitor.add_ip(test_ip, "Test Device")
        
        # Use the mock_network fixture directly - it's already set up to recover after 2 attempts
        monitor._cached_ping = mock_network.side_effect
        
        # Initial check should fail
        try:
            result = await asyncio.wait_for(monitor.check_ip(test_ip), timeout=1.0)
            assert not result[1], "Device should be offline initially"
        except asyncio.TimeoutError:
            print("Initial check timed out as expected")
            result = (test_ip, False, None)
        
        # Attempt recovery with explicit timeout
        try:
            recovered = await asyncio.wait_for(monitor.recover_connection(test_ip), timeout=5.0)
            assert recovered, "Connection should recover after retries"
            
            # Verify recovery status
            status = monitor.get_recovery_status(test_ip)
            assert status['attempts'] > 0, "Recovery attempts should be tracked"
            assert status['recovered'], "Recovery status should indicate success"
        except asyncio.TimeoutError:
            pytest.fail("Recovery attempt timed out")
    finally:
        # Cleanup
        if monitor:
            monitor.stop_discovery()  # Stop any running tasks
            await asyncio.sleep(0.1)  # Give tasks time to clean up

@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_recovery_limits(mock_network):
    """Test recovery attempt limits"""
    monitor = NetworkMonitor(test_mode=True)
    test_ip = "192.168.1.2"
    monitor.add_ip(test_ip, "Test Device")
    
    # Mock ping to always fail
    monitor._cached_ping = lambda *args, **kwargs: None
    
    # Attempt recovery
    recovered = await monitor.recover_connection(test_ip)
    assert not recovered, "Recovery should fail after max attempts"
    
    # Verify attempt count
    status = monitor.get_recovery_status(test_ip)
    assert status['attempts'] == monitor._max_recovery_attempts, "Should stop after max attempts"
    assert not status['recovered'], "Recovery status should indicate failure"

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_concurrent_recovery(mock_network):
    """Test concurrent recovery operations"""
    monitor = NetworkMonitor(test_mode=True)
    test_ips = ["192.168.1.3", "192.168.1.4"]
    for ip in test_ips:
        monitor.add_ip(ip, f"Test Device {ip}")
    
    # Use the mock_network fixture directly - it's already set up to recover after 2 attempts
    monitor._cached_ping = mock_network.side_effect
    
    # Start concurrent recovery attempts
    tasks = [monitor.recover_connection(ip) for ip in test_ips]
    results = await asyncio.gather(*tasks)
    
    # Verify results
    assert results[0], f"Recovery for {test_ips[0]} should succeed"
    assert not results[1], f"Recovery for {test_ips[1]} should fail"
    
    # Verify recovery status for both IPs
    for i, ip in enumerate(test_ips):
        status = monitor.get_recovery_status(ip)
        assert status['attempts'] > 0, f"Recovery attempts for {ip} should be tracked"
        assert status['recovered'] == results[i], f"Recovery status for {ip} should match result"

if __name__ == "__main__":
    pytest.main(["-v", "test_recovery.py"])
