import asyncio
import logging
from datetime import datetime, timedelta
from network_monitor.core.alert_manager import AlertManager

async def test_alert_verification():
    """Verify alert manager functionality"""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    manager = AlertManager()
    test_ip = '192.168.1.1'
    
    logger.info('Testing first-time online notification...')
    await manager.handle_ip_status_change(test_ip, True, 50.0)
    assert test_ip in manager._first_seen, "First-time online notification failed"
    
    logger.info('Testing 24-hour reconnection...')
    manager._last_online[test_ip] = datetime.now() - timedelta(hours=25)
    await manager.handle_ip_status_change(test_ip, True, 50.0)
    assert (datetime.now() - manager._last_online[test_ip]).total_seconds() < 1, "24-hour reconnection failed"
    
    logger.info('Testing offline notifications...')
    await manager.handle_ip_status_change(test_ip, False, None)
    assert test_ip in manager._disconnect_history, "Offline notification failed"
    
    logger.info('Testing frequent disconnection...')
    for i in range(5):
        logger.debug(f'Disconnect/reconnect cycle {i+1}')
        await manager.handle_ip_status_change(test_ip, False, None)
        await asyncio.sleep(0.1)
        await manager.handle_ip_status_change(test_ip, True, 50.0)
        await asyncio.sleep(0.1)
    
    assert manager._disconnect_counts[test_ip] >= 5, "Frequent disconnection detection failed"
    
    logger.info('All verifications completed successfully')

if __name__ == '__main__':
    asyncio.run(test_alert_verification())
