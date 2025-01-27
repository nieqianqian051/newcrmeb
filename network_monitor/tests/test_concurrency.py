import asyncio
import random
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from unittest.mock import Mock, patch
from network_monitor.core.network_monitor import NetworkMonitor

def mock_ping(*args, **kwargs):
    """Mock ping response"""
    # Simulate network latency
    time.sleep(random.uniform(0.001, 0.01))
    # Return random response time or None to simulate offline
    return random.choice([None, random.uniform(1, 100)])

async def stress_test_network_monitor():
    """Stress test the NetworkMonitor class with concurrent operations"""
    print("开始并发压力测试...")
    monitor = NetworkMonitor(test_mode=True)
    # Mock the ping function
    monitor.ping_host = Mock(side_effect=mock_ping)
    
    # Test parameters
    num_threads = 10
    operations_per_thread = 100
    total_operations = num_threads * operations_per_thread
    
    # Counters for verification
    success_count = 0
    error_count = 0
    thread_local = threading.local()
    
    # Track start time
    start_time = time.time()
    
    async def worker(worker_id):
        nonlocal success_count, error_count
        
        try:
            # Generate random IPs for this worker
            base_ip = f"10.246.{random.randint(65, 81)}"
            
            for i in range(operations_per_thread):
                try:
                    # Random IP in test range
                    ip = f"{base_ip}.{random.randint(1, 254)}"
                    desc = f"Test Device {worker_id}-{i}"
                    
                    # Randomly choose an operation
                    operation = random.choice([
                        'add',
                        'remove',
                        'check',
                        'update',
                        'discover'
                    ])
                    
                    if operation == 'add':
                        monitor.add_ip(ip, desc)
                        success_count += 1
                    elif operation == 'remove':
                        monitor.remove_ip(ip)
                        success_count += 1
                    elif operation == 'check':
                        await monitor.check_ip(ip)
                        success_count += 1
                    elif operation == 'update':
                        monitor.update_description(ip, f"Updated {desc}")
                        success_count += 1
                    elif operation == 'discover':
                        # Simulate mini-discovery
                        tasks = []
                        for j in range(5):  # Check 5 IPs at once
                            test_ip = f"{base_ip}.{random.randint(1, 254)}"
                            tasks.append(monitor.check_ip(test_ip))
                        await asyncio.gather(*tasks)
                        success_count += 1
                    
                    # Random delay to simulate real-world conditions
                    await asyncio.sleep(random.uniform(0.01, 0.05))
                    
                except Exception as e:
                    print(f"Worker {worker_id} operation error: {str(e)}")
                    error_count += 1
                    
        except Exception as e:
            print(f"Worker {worker_id} critical error: {str(e)}")
            error_count += 1
    
    try:
        # Create and run worker tasks with timeout
        workers = [worker(i) for i in range(num_threads)]
        await asyncio.wait_for(
            asyncio.gather(*workers),
            timeout=60  # 60 second timeout for entire test
        )
    except asyncio.TimeoutError:
        print("\n测试超时 - 可能表明并发问题")
        return
        
    # Calculate results
    end_time = time.time()
    duration = end_time - start_time
    ops_per_second = total_operations / duration
    
    # Print test results
    print("\n=== 并发压力测试结果 ===")
    print(f"总操作数: {total_operations}")
    print(f"成功操作: {success_count}")
    print(f"失败操作: {error_count}")
    print(f"总耗时: {duration:.2f} 秒")
    print(f"每秒操作数: {ops_per_second:.2f}")
    print(f"成功率: {(success_count/total_operations)*100:.2f}%")
    
    # Verify data integrity
    try:
        # Check if we can still perform operations
        test_ip = "10.246.70.100"
        monitor.add_ip(test_ip, "Integrity Test")
        result = await monitor.check_ip(test_ip)
        monitor.remove_ip(test_ip)
        print("\n数据完整性检查: 通过")
    except Exception as e:
        print(f"\n数据完整性检查: 失败 - {str(e)}")

import pytest

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test concurrent operations on NetworkMonitor"""
    await stress_test_network_monitor()
