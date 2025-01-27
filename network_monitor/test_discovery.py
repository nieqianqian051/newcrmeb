import asyncio
import logging
import unittest.mock
from network_monitor.core.network_monitor import NetworkMonitor

# Mock successful ping responses for specific test IPs
TEST_RESPONDING_IPS = {
    '10.246.65.3': True,
    '10.246.65.7': True,
    '10.246.65.9': True
}

def mock_ping(*args, **kwargs):
    """Mock ping response for testing"""
    ip = args[0]
    # Return a mock response time (50ms) for online IPs, None for offline
    return 50.0 if TEST_RESPONDING_IPS.get(ip, False) else None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_discovery():
    # Initialize network monitor in test mode
    monitor = NetworkMonitor(test_mode=True)
    
    # Mock ping responses for testing
    monitor.ping_host = unittest.mock.Mock(side_effect=mock_ping)
    print("\nMocked responses configured for IPs:")
    for ip, status in TEST_RESPONDING_IPS.items():
        print(f"- {ip}: {'在线' if status else '离线'}")
    
    # Set discovery range (using smaller test range)
    monitor.set_discovery_range('10.246.65.1', '10.246.65.10')  # Test with 10 IPs first
    
    # Set discovery interval (using default 5 minutes)
    monitor.set_discovery_interval(300)
    
    print("\n=== Starting IP Discovery Test ===")
    print(f"Scan Range: {monitor.discovery_start_ip} - {monitor.discovery_end_ip}")
    print(f"Scan Interval: {monitor.discovery_interval} seconds")
    
    # Run a single discovery scan
    print("\nRunning discovery scan...")
    discovered = await monitor.discover_ips()
    
    print(f"\nDiscovered {discovered} new devices")
    if discovered > 0:
        print("\nDiscovered IPs:")
        for ip, desc in monitor.ip_data.items():
            if '自动发现' in desc:
                print(f"- {ip}: {desc}")
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    asyncio.run(test_discovery())
