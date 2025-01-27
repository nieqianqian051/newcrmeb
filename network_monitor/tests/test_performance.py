import asyncio
import time
import os
import json
import gzip
from datetime import datetime
from network_monitor.core.network_monitor import NetworkMonitor
from network_monitor.core.backup_manager import BackupManager

import pytest

@pytest.mark.asyncio
async def test_ip_conversion_performance():
    """Test performance of IP address conversion with caching"""
    monitor = NetworkMonitor(test_mode=True)
    
    # Test data
    test_ips = [f"192.168.1.{i}" for i in range(256)]
    
    # Test without cache (clear cache first)
    monitor._ip_to_int.cache_clear()
    start_time = time.time()
    for ip in test_ips:
        _ = monitor._ip_to_int(ip)
    uncached_time = time.time() - start_time
    
    # Test with cache
    start_time = time.time()
    for ip in test_ips:
        _ = monitor._ip_to_int(ip)
    cached_time = time.time() - start_time
    
    print(f"\nIP转换性能测试:")
    print(f"未缓存时间: {uncached_time:.4f}秒")
    print(f"缓存时间: {cached_time:.4f}秒")
    print(f"性能提升: {((uncached_time - cached_time) / uncached_time * 100):.1f}%")
    
    assert cached_time < uncached_time, "缓存应该提高性能"

@pytest.mark.asyncio
async def test_backup_compression():
    """Test backup compression effectiveness"""
    backup_dir = "test_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create test data
    test_data = {
        f"192.168.1.{i}": f"Test Device {i}" * 10  # Make descriptions longer for better compression
        for i in range(100)
    }
    
    backup_manager = BackupManager(backup_dir=backup_dir)
    
    # Test uncompressed backup
    uncompressed_file = os.path.join(backup_dir, "backup_uncompressed.json")
    with open(uncompressed_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    uncompressed_size = os.path.getsize(uncompressed_file)
    
    # Test compressed backup
    compressed_file = os.path.join(backup_dir, "backup_compressed.json.gz")
    with gzip.open(compressed_file, "wt", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)
    compressed_size = os.path.getsize(compressed_file)
    
    print(f"\n备份压缩测试:")
    print(f"未压缩大小: {uncompressed_size / 1024:.1f} KB")
    print(f"压缩后大小: {compressed_size / 1024:.1f} KB")
    print(f"压缩率: {((uncompressed_size - compressed_size) / uncompressed_size * 100):.1f}%")
    
    # Verify data integrity
    with gzip.open(compressed_file, "rt", encoding="utf-8") as f:
        restored_data = json.load(f)
    assert restored_data == test_data, "压缩数据应该能够正确还原"
    
    # Clean up test files
    os.remove(uncompressed_file)
    os.remove(compressed_file)
    os.rmdir(backup_dir)

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_ping_cache_performance():
    """Test ping caching performance"""
    monitor = NetworkMonitor(test_mode=True)
    test_ip = "192.168.1.1"
    iterations = 5  # Reduced iterations for faster test
    
    try:
        # Test without cache
        monitor._cached_ping.cache_clear()
        start_time = time.time()
        for _ in range(iterations):
            try:
                await asyncio.wait_for(monitor.check_ip(test_ip), timeout=0.5)
            except asyncio.TimeoutError:
                print("Ping timeout as expected")
        uncached_time = time.time() - start_time
        
        # Test with cache (should use cached results)
        start_time = time.time()
        for _ in range(iterations):
            try:
                await asyncio.wait_for(monitor.check_ip(test_ip), timeout=0.5)
            except asyncio.TimeoutError:
                print("Ping timeout as expected")
        cached_time = time.time() - start_time
        
        print(f"\nPing缓存性能测试:")
        print(f"未缓存时间: {uncached_time:.4f}秒")
        print(f"缓存时间: {cached_time:.4f}秒")
        print(f"性能提升: {((uncached_time - cached_time) / uncached_time * 100):.1f}%")
        
        assert cached_time < uncached_time, "缓存应该提高性能"
    finally:
        if monitor:
            monitor.stop_discovery()  # Stop any running tasks
            await asyncio.sleep(0.1)  # Give tasks time to clean up
    
    print(f"\nPing缓存性能测试:")
    print(f"未缓存时间: {uncached_time:.4f}秒")
    print(f"缓存时间: {cached_time:.4f}秒")
    print(f"性能提升: {((uncached_time - cached_time) / uncached_time * 100):.1f}%")
    
    assert cached_time < uncached_time, "缓存应该提高性能"

async def main():
    """Run all performance tests"""
    print("开始性能测试...")
    
    await test_ip_conversion_performance()
    await test_backup_compression()
    await test_ping_cache_performance()
    
    print("\n所有性能测试完成!")

if __name__ == "__main__":
    asyncio.run(main())
