import pytest
import pytest_asyncio
import asyncio
import time
import aiohttp
import logging
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from network_monitor.core.network_monitor import NetworkMonitor
from network_monitor.core.alert_manager import AlertManager, AlertLevel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest_asyncio.fixture
async def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    
    try:
        # Clean up all remaining tasks
        pending = asyncio.all_tasks(loop)
        if pending:
            logger.debug(f"Cleaning up {len(pending)} pending tasks")
            for task in pending:
                if not task.done():
                    logger.debug(f"Cancelling task: {task.get_name()}")
                    task.cancel()
            
            # Wait with timeout for tasks to clean up
            try:
                await asyncio.wait_for(
                    asyncio.gather(*pending, return_exceptions=True),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for tasks to clean up")
            except Exception as e:
                logger.warning(f"Error during task cleanup: {str(e)}")
    finally:
        # Always try to clean up the loop
        try:
            await loop.shutdown_asyncgens()
        except Exception as e:
            logger.warning(f"Error during asyncgen shutdown: {str(e)}")
        finally:
            loop.close()

@pytest_asyncio.fixture
async def mock_requests():
    """Mock aiohttp ClientSession for webhook testing"""
    class MockResponse:
        def __init__(self, status=200, response_text='{"errcode":0,"errmsg":"ok"}'):
            self._status = status
            self._text = response_text
            self._closed = False
            logger.debug(f"Creating MockResponse with status {status}")
            
        async def __aenter__(self):
            logger.debug("Entering MockResponse context")
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            logger.debug("Exiting MockResponse context")
            await self.aclose()
            return None  # Don't suppress exceptions
            
        async def text(self):
            return self._text
            
        @property
        def status(self):
            return self._status
            
        async def aclose(self):
            if not self._closed:
                self._closed = True
                logger.debug("Closing MockResponse")
            
        def close(self):
            pass  # For compatibility with non-async code
    
    async def mock_post(*args, **kwargs):
        """Mock webhook response that returns an awaitable"""
        # Track the call first
        mock_post.called = True
        mock_post.call_count += 1
        mock_post.call_args = (args, kwargs)
        mock_post.call_args_list.append((args, kwargs))
        
        # Create response object
        # Extract URL from kwargs since we're using explicit url parameter
        url = kwargs.get('url', '')
        logger.debug(f"Mock received URL: {url}")
        
        # Create response based on request validation
        webhook_key = '95bdf169-37a5-4465-8c8b-a041c2dde85a'
        if not url or webhook_key not in url:
            logger.debug(f"Invalid webhook key. URL: {url}")
            return MockResponse(400, '{"errcode":40001,"errmsg":"invalid webhook key"}')
            
        # Validate payload
        payload = kwargs.get('json', {})
        logger.debug(f"Mock received payload: {payload}")
        
        if not payload.get('msgtype') == 'text' or 'text' not in payload:
            logger.debug("Invalid message format")
            return MockResponse(400, '{"errcode":40002,"errmsg":"invalid message format"}')
            
        # Valid request
        logger.debug("Valid request, returning success")
        return MockResponse(200, '{"errcode":0,"errmsg":"ok"}')
    
    # Create mock with direct function assignment and proper initialization
    mock_post.called = False
    mock_post.call_count = 0
    mock_post.call_args = None
    mock_post.call_args_list = []
    
    # Create a proper Mock-like reset function
    def reset_mock():
        mock_post.called = False
        mock_post.call_count = 0
        mock_post.call_args = None
        mock_post.call_args_list = []
    
    mock_post.reset_mock = reset_mock
    
    # Patch the session's post method
    with patch('aiohttp.ClientSession.post', new=mock_post):
        yield mock_post
        
@pytest_asyncio.fixture
async def monitor():
    """Fixture to create a test NetworkMonitor instance"""
    monitor = NetworkMonitor(test_mode=True)
    monitor._cached_ping = AsyncMock(return_value=50.0)  # Default response time
    
    # Configure alert manager for testing
    alert_manager = AlertManager()
    alert_manager._alert_cooldowns = {
        AlertLevel.INFO: 1,      # 1 second for testing
        AlertLevel.WARNING: 1,   # 1 second for testing
        AlertLevel.CRITICAL: 1   # 1 second for testing
    }
    monitor.alert_manager = alert_manager
    
    yield monitor
    
    try:
        # Cleanup with proper task handling and logging
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        logger.debug(f"Cleaning up {len(tasks)} tasks")
        
        # First attempt graceful shutdown
        for task in tasks:
            if not task.done():
                logger.debug(f"Requesting cancellation of task: {task.get_name()}")
                task.cancel()
        
        if tasks:
            # Wait briefly for tasks to clean up
            try:
                await asyncio.wait(tasks, timeout=1.0)
            except (asyncio.CancelledError, Exception) as e:
                logger.debug(f"Expected cleanup exception: {str(e)}")
                
            # Force cancel any remaining tasks
            for task in tasks:
                if not task.done():
                    logger.debug(f"Force cancelling task: {task.get_name()}")
                    task.cancel()
                    try:
                        await asyncio.wait([task], timeout=0.1)
                    except Exception:
                        pass
                        
    except Exception as e:
        logger.error(f"Error during monitor fixture cleanup: {str(e)}")
    finally:
        # Break circular references
        if hasattr(monitor, 'alert_manager'):
            logger.debug("Cleaning up alert manager")
            monitor.alert_manager = None
        if hasattr(monitor, 'executor'):
            logger.debug("Shutting down executor")
            monitor.executor.shutdown(wait=False)
            
        # Force garbage collection
        import gc
        gc.collect()

# Mock network operations
@pytest_asyncio.fixture
async def mock_network():
    """Mock network operations for testing"""
    async def mock_ping(*args, **kwargs):
        ip = args[0] if args else kwargs.get('ip')
        test_ips = {
            '192.168.1.1': 50.0,
            '192.168.1.2': 50.0,
            '10.246.65.1': 45.0,
            '10.246.81.254': 55.0
        }
        return test_ips.get(ip, None)
    
    with patch('network_monitor.core.network_monitor.NetworkMonitor._cached_ping', 
               new=mock_ping) as mock:
        yield mock

@pytest.mark.asyncio
@pytest.mark.timeout(30)  # Increased timeout for stability
async def test_alert_system(mock_requests, monitor):
    """Test alert system functionality according to requirements"""
    logger.info("Starting alert system test")
    
    # Test setup
    test_ip = "192.168.1.1"
    monitor.add_ip(test_ip, "Test Device")
    logger.info(f"Added test IP: {test_ip}")
    
    # Enable test mode and configure for testing
    monitor.alert_manager._test_mode = True
    monitor.alert_manager._alert_cooldowns = {
        AlertLevel.INFO: 0,
        AlertLevel.WARNING: 0,
        AlertLevel.CRITICAL: 0
    }
    
    # Configure detailed logging
    monitor.alert_manager.logger.setLevel(logging.DEBUG)
    
    # Test first-time online notification
    logger.info("Testing first-time online notification")
    monitor._cached_ping = AsyncMock(return_value=50.0)
    
    # Reset state
    mock_requests.reset_mock()
    
    if test_ip in monitor.alert_manager._first_seen:
        del monitor.alert_manager._first_seen[test_ip]
        
    # Send notification
    logger.debug("Triggering first-time online notification")
    await monitor.alert_manager.handle_ip_status_change(test_ip, True, 50.0)
    
    # Quick verification
    assert mock_requests.called, "First-time online notification not sent"
    assert mock_requests.call_args is not None, "Webhook call arguments not captured"
    assert "首次上线" in mock_requests.call_args[1]['json']['text']['content'], "Wrong notification content"
    
    # Test 24-hour reconnection
    logger.info("Testing 24-hour reconnection notification")
    monitor.alert_manager._last_online[test_ip] = datetime.now() - timedelta(hours=25)
    
    mock_requests.reset_mock()
    await monitor.alert_manager.handle_ip_status_change(test_ip, True, 50.0)
    assert mock_requests.called, "24-hour reconnection notification not sent"
    
    # Test offline notification
    logger.info("Testing offline notification")
    mock_requests.reset_mock()
    await monitor.alert_manager.handle_ip_status_change(test_ip, False, None)
    assert mock_requests.called, "Offline notification not sent"
    
    # Test frequent disconnection detection
    logger.info("Testing frequent disconnection detection")
    
    # Reset disconnect history and count
    monitor.alert_manager._disconnect_history[test_ip] = []
    monitor.alert_manager._disconnect_counts[test_ip] = 0
    monitor.alert_manager._last_state[test_ip] = True  # Start in online state
    
    # Mock time to simulate longer intervals between disconnections
    base_time = datetime(2025, 1, 27, 6, 0, 0)  # Fixed start time
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now = Mock()  # Create a mock for the now() method
        
        for i in range(5):
            logger.debug(f"\nDisconnect cycle {i+1}")
            current_time = base_time + timedelta(minutes=i*7)  # 7 minutes between cycles
            
            # Log initial state
            logger.debug(f"Before cycle - state: {monitor.alert_manager._last_state.get(test_ip)}, count: {monitor.alert_manager._disconnect_counts.get(test_ip, 0)}")
            
            # Go offline
            mock_datetime.now.return_value = current_time
            await monitor.alert_manager.handle_ip_status_change(test_ip, False, None)
            
            # Log state after going offline
            logger.debug(f"After offline - state: {monitor.alert_manager._last_state.get(test_ip)}, count: {monitor.alert_manager._disconnect_counts.get(test_ip, 0)}")
            
            # Verify offline state and count
            assert not monitor.alert_manager._last_state.get(test_ip), f"Device should be offline in cycle {i+1}"
            assert monitor.alert_manager._disconnect_counts.get(test_ip, 0) == i + 1, f"Disconnect count should be {i + 1}"
            
            # Come back online after 6 minutes
            mock_datetime.now.return_value = current_time + timedelta(minutes=6)
            await monitor.alert_manager.handle_ip_status_change(test_ip, True, 50.0)
            
            # Log state after cycle
            logger.debug(f"After cycle {i+1} - state: {monitor.alert_manager._last_state.get(test_ip)}, count: {monitor.alert_manager._disconnect_counts.get(test_ip, 0)}")
            logger.debug(f"History size: {len(monitor.alert_manager._disconnect_history[test_ip])}")
            
            # Verify online state
            assert monitor.alert_manager._last_state.get(test_ip), f"Device should be online after cycle {i+1}"
            
        # Verify final state
        assert monitor.alert_manager._disconnect_counts[test_ip] == 5, "Should have recorded 5 disconnections"
        assert len(monitor.alert_manager._disconnect_history[test_ip]) == 5, "Should have 5 disconnect events in history"
    
    # Final offline state
    await monitor.alert_manager.handle_ip_status_change(test_ip, False, None)
    
    # Log final state
    logger.debug(f"Final disconnect count: {monitor.alert_manager._disconnect_counts[test_ip]}")
    
    # Verify frequent disconnection detection
    assert monitor.alert_manager._disconnect_counts[test_ip] >= 5, "Frequent disconnection not detected"
    
    # Verify that the appropriate alert was sent during the disconnect cycles
    found_frequent_alert = False
    for args, kwargs in mock_requests.call_args_list:
        if 'json' in kwargs and '频繁断线' in kwargs['json']['text']['content']:
            found_frequent_alert = True
            break
    assert found_frequent_alert, "Frequent disconnection alert not sent"
    
    # Cleanup
    monitor.alert_manager._test_mode = False
        
    # Removed duplicate test code - using the first test section which is more concise

@pytest.mark.asyncio
@pytest.mark.timeout(60)  # Increased timeout for stability
async def test_alert_manager(mock_requests):
    """Test AlertManager functionality"""
    manager = AlertManager()
    test_ip = "192.168.1.1"
    
    try:
        # Enable test mode to bypass locks
        manager._test_mode = True
        
        # Test first-time online notification
        await manager.handle_ip_status_change(test_ip, True, 50.0)
        assert test_ip in manager._first_seen, "Should track first-time online"
        
        # Test 24-hour reconnection
        # Set last online to 25 hours ago
        manager._last_online[test_ip] = datetime.now() - timedelta(hours=25)
        await manager.handle_ip_status_change(test_ip, True, 50.0)
        assert (datetime.now() - manager._last_online[test_ip]).total_seconds() < 1, "Should update last online time"
        
        # Test offline alerts with 5-minute interval
        await manager.handle_ip_status_change(test_ip, False, None)
        first_alert_time = datetime.now()
        assert test_ip in manager._disconnect_history, "Should track disconnection"
        
        # Test alert suppression within 5-minute window
        await manager.handle_ip_status_change(test_ip, False, None)
        assert len(manager._disconnect_history[test_ip]) == 1, "Should not add duplicate alerts within 5 minutes"
        
        # Test frequent disconnection detection
        # Reset disconnect history and count
        manager._disconnect_history[test_ip] = []
        manager._disconnect_counts[test_ip] = 0
        manager._last_state[test_ip] = True  # Start in online state
        
        # Mock time to simulate longer intervals between disconnections
        base_time = datetime(2025, 1, 27, 6, 0, 0)  # Fixed start time
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now = Mock()  # Create a mock for the now() method
            
            for i in range(5):
                current_time = base_time + timedelta(minutes=i*7)  # 7 minutes between cycles
                mock_datetime.now.return_value = current_time
                
                # Go offline
                await manager.handle_ip_status_change(test_ip, False, None)
                
                # Come back online after 6 minutes
                mock_datetime.now.return_value = current_time + timedelta(minutes=6)
                await manager.handle_ip_status_change(test_ip, True, 50.0)
            
            # Final offline state
            mock_datetime.now.return_value = base_time + timedelta(minutes=35)
            await manager.handle_ip_status_change(test_ip, False, None)
            
            assert manager._disconnect_counts[test_ip] >= 5, "Should detect frequent disconnections"
        
        # Test disconnection reason analysis
        # Test high latency
        await manager.handle_ip_status_change(test_ip, False, 1500.0)  # 1.5 second response
        assert "网络延迟过高" in manager._analyze_disconnect_reason(test_ip, 1500.0)
        
        # Test unstable network
        manager._disconnect_history[test_ip] = [
            datetime.now() - timedelta(minutes=i*5)
            for i in range(3)  # 3 disconnects in short period
        ]
        assert "网络不稳定" in manager._analyze_disconnect_reason(test_ip, None)
        
        # Test basic disconnection
        manager._disconnect_history[test_ip] = [datetime.now()]
        assert "网络连接中断" in manager._analyze_disconnect_reason(test_ip, None)
        
    finally:
        # Cleanup
        manager._test_mode = False
        # Cancel any pending tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.wait(tasks, timeout=1.0)

@pytest.mark.asyncio
async def test_alert_channels(mock_requests):
    """Test alert channels and routing"""
    manager = AlertManager()
    
    # Test default channels
    assert "wechat" in manager._alert_channels[AlertLevel.INFO]
    assert "sound" in manager._alert_channels[AlertLevel.WARNING]
    assert all(ch in manager._alert_channels[AlertLevel.CRITICAL] 
              for ch in ["wechat", "sound", "ui"])
    
    # Test channel modification
    test_channel = "test_channel"
    await manager.add_channel(AlertLevel.INFO, test_channel)
    assert test_channel in manager._alert_channels[AlertLevel.INFO]
    
    await manager.remove_channel(AlertLevel.INFO, test_channel)
    assert test_channel not in manager._alert_channels[AlertLevel.INFO]
    
    # Test webhook functionality
    test_message = "Test webhook message"
    try:
        # Reset mock state
        mock_requests.reset_mock()
        
        # Send alert
        assert await manager.send_alert(test_message, AlertLevel.INFO)
        
        # Verify call
        assert mock_requests.called, "Webhook should have been called"
        assert mock_requests.call_count == 1, "Webhook should have been called exactly once"
        assert mock_requests.call_args is not None, "Call arguments should be recorded"
        assert mock_requests.call_args[1]['json']['text']['content'] == manager._format_alert(test_message, AlertLevel.INFO)
    except Exception as e:
        print(f"Error testing webhook: {str(e)}")
        raise

    # Clean up any pending tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

@pytest.mark.asyncio
@pytest.mark.timeout(10)  # Reduced timeout since we're optimizing
async def test_batch_alerts(mock_network, mock_requests):
    """Test handling multiple alerts in batch"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Clear any existing IPs and tasks
    monitor._ip_data.clear()
    monitor._tasks.clear()
    
    try:
        # Add test devices one at a time to avoid task buildup
        test_ips = {
            "192.168.1.1": "Test Device 1",
            "192.168.1.2": "Test Device 2",
            "192.168.1.3": "Test Device 3"
        }
        
        for ip, desc in test_ips.items():
            monitor.add_ip(ip, desc)
            await asyncio.sleep(0)  # Allow event loop to process
        
        # Mock network responses with controlled timing
        async def mock_ping_all_offline(*args, **kwargs):
            await asyncio.sleep(0.1)  # Small delay to simulate network
            return None
            
        async def mock_ping_selective(*args, **kwargs):
            await asyncio.sleep(0.1)  # Small delay to simulate network
            ip = args[0] if args else kwargs.get('ip', '')
            return 50.0 if ip in ["192.168.1.1", "192.168.1.2"] else None
        
        # Test offline state
        monitor._cached_ping = mock_ping_all_offline
        results = await asyncio.wait_for(monitor.check_all_ips(), timeout=5.0)
        assert all(not status for status in results.values()), "All devices should be offline"
        
        # Test mixed state
        monitor._cached_ping = mock_ping_selective
        results = await asyncio.wait_for(monitor.check_all_ips(), timeout=5.0)
        assert results["192.168.1.1"], "Device 1 should be online"
        assert results["192.168.1.2"], "Device 2 should be online"
        assert not results["192.168.1.3"], "Device 3 should be offline"
        
    except asyncio.TimeoutError:
        print("Test timed out - this may indicate a performance issue")
        raise
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        raise
    finally:
        # Improved task cleanup
        try:
            tasks = [t for t in asyncio.all_tasks() 
                    if t is not asyncio.current_task() and not t.done()]
            if tasks:
                print(f"Cleaning up {len(tasks)} pending tasks")
                for task in tasks:
                    task.cancel()
                await asyncio.wait(tasks, timeout=1.0)
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            # Don't raise cleanup errors

if __name__ == "__main__":
    pytest.main(["-v", "test_alerts.py"])
