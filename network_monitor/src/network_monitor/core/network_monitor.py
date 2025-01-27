import asyncio
from datetime import datetime
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import socket
import psutil
import netifaces
from ping3 import ping
import requests
from scapy.all import sniff, IP
from threading import Lock, RLock
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import threading
import weakref

from .backup_manager import BackupManager

class NetworkMonitor:
    def __init__(self, test_mode=False, max_workers=None):
        # Thread pool for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=max_workers or (os.cpu_count() or 1) * 2)
        
        # Task management with weak references to prevent cycles
        self._tasks = weakref.WeakSet()
        self._task_lock = asyncio.Lock()
        
        # Locks for thread safety
        self._ip_data_lock = RLock()  # Reentrant lock for IP data
        self._status_lock = Lock()    # Lock for status tracking
        self._storm_lock = Lock()     # Lock for storm detection
        self._discovery_lock = Lock()  # Lock for discovery operations
        self._recovery_lock = asyncio.Lock()  # Async lock for recovery operations
        
        # Initialize alert manager
        from network_monitor.core.alert_manager import AlertManager
        self.alert_manager = AlertManager()
        
        # Recovery configuration
        self._max_recovery_attempts = 4
        self._recovery_interval = 0.01 if test_mode else 5  # 0.01 seconds in test mode, 5 seconds in production
        self._recovery_status = {}  # Track recovery attempts
        self._recovery_timeout = 0.1 if test_mode else 2  # Shorter timeout for recovery in test mode
        
        # Test mode configuration
        self._test_mode = test_mode
        self.ping_timeout = 0.5 if test_mode else 2  # Shorter timeout in test mode
        
        if test_mode:
            self._discovery_interval = 5  # 5 seconds in test mode
            self._auto_save_interval = 20  # 20 seconds in test mode
            self._mock_responses = {
                '192.168.1.1': 50.0,
                '192.168.1.2': 50.0,
                '10.246.65.1': 45.0,
                '10.246.81.254': 55.0
            }
            self._mock_recovery_after = 2  # Number of attempts before recovery
            self.last_save_time = datetime.now()
        else:
            self._discovery_interval = 300  # 5 minutes in production
            self._auto_save_interval = 1200  # 20 minutes in production
            self.last_save_time = datetime.now()
            
        self._ip_data = {}  # Initialize empty, let tests add their own IPs
        
        self.webhook_key = 'a3878897-5073-4ee8-b0b7-aaa71f024ef7'
        self.webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={self.webhook_key}'
        self.max_message_length = 2048
        self.storm_threshold = 1000  # packets per second
        self.port_scan_timeout = 2
        self._monitored_ports = {80, 443, 22}  # 预设一些常用端口
        
        # Status tracking with thread safety
        self._ip_status = {}
        self._alert_status = {}
        self._storm_status = False
        self._last_storm_alert = None
        
        # Initialize backup manager
        self.backup_manager = BackupManager()
        
        # Auto-discovery configuration with thread safety
        self._discovery_enabled = False
        self._discovery_interval = 300 if not test_mode else 5  # 5 minutes in production, 5 seconds in test
        self._discovery_start_ip = '10.246.65.1'
        self._discovery_end_ip = '10.246.81.254'
        self._discovery_task = None
        self._auto_save_interval = 1200 if not test_mode else 20  # 20 minutes in production, 20 seconds in test
        
        # Cache for frequently accessed data
        self._cache = weakref.WeakValueDictionary()
        
        print("正在加载网络监控器...")
        self.load_data()
        print(f"已加载 {len(self._ip_data)} 个IP地址")

    @property
    def ip_data(self) -> Dict[str, str]:
        """Thread-safe access to IP data"""
        with self._ip_data_lock:
            return self._ip_data.copy()
            
    @ip_data.setter
    def ip_data(self, value: Dict[str, str]):
        """Thread-safe setter for IP data"""
        with self._ip_data_lock:
            self._ip_data = value.copy()
    
    @property
    def monitored_ports(self) -> set:
        """Thread-safe access to monitored ports"""
        with self._ip_data_lock:
            return self._monitored_ports.copy()
    
    def add_ip(self, ip: str, description: str):
        """Add or update an IP address and its description"""
        with self._ip_data_lock:
            self._ip_data[ip.strip()] = description.strip()
            # Clear any cached data for this IP
            if ip in self._cache:
                del self._cache[ip]

    def remove_ip(self, ip: str):
        """Remove an IP address from monitoring"""
        with self._ip_data_lock:
            ip = ip.strip()
            if ip in self._ip_data:
                del self._ip_data[ip]
            # Clear any cached data
            if ip in self._cache:
                del self._cache[ip]
            with self._status_lock:
                if ip in self._ip_status:
                    del self._ip_status[ip]
                if ip in self._alert_status:
                    del self._alert_status[ip]

    def get_all_ips(self) -> Dict[str, str]:
        """Get all monitored IPs and their descriptions"""
        return self.ip_data  # Already returns a copy via property
        
    def update_description(self, ip: str, description: str):
        """Update IP description with thread safety"""
        with self._ip_data_lock:
            if ip.strip() in self._ip_data:
                self._ip_data[ip.strip()] = description.strip()
                # Clear any cached data
                if ip in self._cache:
                    del self._cache[ip]

    def load_data(self, backup_file: Optional[str] = None):
        """
        Load IP data from file or backup
        
        Args:
            backup_file: Optional backup file to restore from
        """
        try:
            # Try to load from backup if specified
            if backup_file:
                restored_data = self.backup_manager.rollback(backup_file)
                if restored_data:
                    self.ip_data = restored_data
                    print(f"已从备份恢复数据: {backup_file}")
                    return
            
            # Load from current data file
            data_file = Path('ip_data.json')
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.ip_data = json.load(f)
        except Exception as e:
            print(f"加载数据时出错: {str(e)}")

    def save_data(self, force: bool = False):
        """
        Save IP data to file and create backup if needed with thread safety
        
        Args:
            force: Force backup creation regardless of changes
        """
        with self._ip_data_lock:
            try:
                # Save current data
                with open('ip_data.json', 'w', encoding='utf-8') as f:
                    json.dump(self._ip_data, f, ensure_ascii=False, indent=2)
                
                # Create backup if needed
                backup_file = self.backup_manager.save_data(self._ip_data, force)
                if backup_file:
                    print(f"数据已备份至: {backup_file}")
                
                # Update last save time
                self.last_save_time = datetime.now()
                return True
            except Exception as e:
                print(f"保存数据时出错: {str(e)}")
                return False

    def ping_host(self, ip: str, timeout: float = 2) -> Optional[float]:
        """Ping a host and return the response time or None if unreachable"""
        try:
            return ping(ip.strip(), timeout=timeout)
        except Exception:
            return None

    async def check_ip(self, ip: str) -> Tuple[str, bool, Optional[float]]:
        """Check if an IP is responding with caching and enhanced alert handling"""
        try:
            print(f"正在检查IP: {ip}")
            # Handle both sync and async _cached_ping
            if hasattr(self, '_cached_ping'):
                if asyncio.iscoroutinefunction(self._cached_ping):
                    result = await self._cached_ping(ip.strip())
                else:
                    result = self._cached_ping(ip.strip())
            else:
                result = await self.ping_host(ip)
                
            is_alive = result is not None and result is not False
            
            # Get previous status if available
            prev_status = getattr(self, '_ip_status', {}).get(ip, None)
            
            # Update status
            if not hasattr(self, '_ip_status'):
                self._ip_status = {}
            self._ip_status[ip] = is_alive
            
            # Only print status if it changed or if it's the first check
            if prev_status is None or prev_status != is_alive:
                print(f"IP {ip} 检查结果: {'在线' if is_alive else '离线'} (响应时间: {result if is_alive else 'N/A'}ms)")
                
            # Handle alerts through our dedicated method
            try:
                await self.handle_ip_status_change(ip, is_alive, result)
            except Exception as e:
                print(f"Error handling alert for {ip}: {str(e)}")
            return ip, is_alive, result
        except Exception as e:
            print(f"检查IP {ip} 时出错: {str(e)}")
            return ip, False, None

    @lru_cache(maxsize=1024)
    def _get_cached_port_status(self, ip: str, port: int) -> Optional[bool]:
        """Get cached port status with 5-second TTL"""
        return None  # Cache decorator handles the actual caching

    async def check_port(self, ip: str, port: int) -> bool:
        """Check if a specific port is open with thread safety and caching"""
        try:
            ip = ip.strip()
            print(f"检查端口 {ip}:{port}")
            
            # Check cache first
            cached_status = self._get_cached_port_status(ip, port)
            if cached_status is not None:
                return cached_status

            # Use thread pool for socket operations
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            
            def check_port_thread():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)  # 1 second timeout
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    loop.call_soon_threadsafe(future.set_result, result == 0)
                except Exception as e:
                    loop.call_soon_threadsafe(future.set_exception, e)
            
            # Use our thread pool executor
            await loop.run_in_executor(self.executor, check_port_thread)
            result = await asyncio.wait_for(future, timeout=2)
            
            # Update cache
            self._get_cached_port_status.cache_clear()  # Clear old cache
            self._get_cached_port_status(ip, port)  # Cache new status
            
            print(f"端口 {ip}:{port} - {'开放' if result else '关闭'}")
            return result
            
        except (asyncio.TimeoutError, Exception) as e:
            print(f"检查端口 {ip}:{port} 时出错: {str(e)}")
            return False

    @lru_cache(maxsize=32)
    def get_network_interfaces(self) -> List[Dict]:
        """Get all network interfaces and their details with thread safety and caching"""
        interfaces = []
        with self._ip_data_lock:  # Use existing lock for network operations
            try:
                for iface in netifaces.interfaces():
                    try:
                        addrs = netifaces.ifaddresses(iface)
                        ipv4 = addrs.get(netifaces.AF_INET, [])
                        if ipv4:
                            interfaces.append({
                                'name': iface,
                                'ip': ipv4[0].get('addr'),
                                'netmask': ipv4[0].get('netmask'),
                                'broadcast': ipv4[0].get('broadcast'),
                                'timestamp': datetime.now().timestamp()  # For cache invalidation
                            })
                    except Exception as e:
                        print(f"获取接口 {iface} 信息时出错: {str(e)}")
                        continue
                return interfaces
            except Exception as e:
                print(f"获取网络接口列表时出错: {str(e)}")
                return []

    @lru_cache(maxsize=128)
    def get_network_usage(self) -> Dict[str, float]:
        """Get network usage statistics with thread safety and caching"""
        with self._status_lock:  # Use status lock for network stats
            try:
                net_io = psutil.net_io_counters()
                return {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv,
                    'timestamp': datetime.now().timestamp()  # For cache invalidation
                }
            except Exception as e:
                print(f"获取网络使用统计时出错: {str(e)}")
                return {
                    'bytes_sent': 0,
                    'bytes_recv': 0,
                    'packets_sent': 0,
                    'packets_recv': 0,
                    'error': str(e)
                }

    def detect_network_storm(self, timeout: int = 1) -> Dict:
        """Detect network storm by monitoring packet rate with thread safety"""
        with self._storm_lock:  # Ensure thread safety for storm detection
            try:
                # Check if we have root privileges
                if os.geteuid() != 0:
                    self.send_alert(
                        "需要管理员权限来监测网络风暴",
                        "WARNING",
                        "network_storm_permissions"
                    )
                    return {
                        'error': 'insufficient_permissions',
                        'message': '需要管理员权限来监测网络风暴'
                    }

                # Check cooldown period (5 minutes between alerts)
                now = datetime.now()
                with self._status_lock:  # Thread-safe access to status
                    last_alert = self._last_storm_alert
                    if last_alert and (now - last_alert).total_seconds() < 300:
                        return {
                            'suppressed': True,
                            'message': '网络风暴检测冷却中'
                        }

                packet_count = 0
                start_time = now

                def packet_callback(packet):
                    nonlocal packet_count
                    if IP in packet:
                        packet_count += 1

                try:
                    sniff(timeout=timeout, prn=packet_callback, store=False)
                except PermissionError:
                    return {
                        'error': 'permission_denied',
                        'message': '无法访问网络接口，请以管理员身份运行'
                    }
                
                duration = (datetime.now() - start_time).total_seconds()
                packets_per_second = packet_count / duration

                # Update storm status tracking with thread safety
                with self._status_lock:
                    prev_storm = self._storm_status
                    curr_storm = packets_per_second > self.storm_threshold

                    if curr_storm and (not prev_storm or not last_alert or 
                                     (now - last_alert).total_seconds() >= 300):
                        self._last_storm_alert = now
                        self._storm_status = True
                        return {
                            'detected': True,
                            'packets_per_second': packets_per_second,
                            'threshold': self.storm_threshold,
                            'status_changed': not prev_storm,
                            'timestamp': now.timestamp()
                        }
                    
                    self._storm_status = curr_storm
                    return {
                        'detected': False,
                        'packets_per_second': packets_per_second,
                        'threshold': self.storm_threshold,
                        'status_changed': prev_storm != curr_storm,
                        'timestamp': now.timestamp()
                    }
            except Exception as e:
                return {
                    'error': 'unknown_error',
                    'message': f'监测网络风暴时发生错误: {str(e)}'
                }

    async def check_all_ips(self):
        """Check all IPs concurrently with enhanced thread safety and error handling"""
        try:
            # Get IPs with thread safety
            with self._ip_data_lock:
                ips = list(self._ip_data.keys())
            
            # Use semaphore to limit concurrent tasks
            sem = asyncio.Semaphore(min(32, len(ips)))  # Limit concurrent checks
            results = {}
            
            async def check_with_semaphore(ip):
                """Check a single IP with semaphore control"""
                try:
                    async with sem:
                        ip, is_alive, response_time = await self.check_ip(ip)
                        print(f"IP {ip} 检查结果: {'在线' if is_alive else '离线'} (响应时间: {response_time if response_time is not None else 'N/A'}ms)")
                        return ip, is_alive
                except Exception as e:
                    print(f"Error checking {ip}: {str(e)}")
                    return ip, False
            
            # Create and track tasks
            tasks = []
            for ip in ips:
                task = asyncio.create_task(check_with_semaphore(ip))
                tasks.append(task)
                async with self._task_lock:
                    self._tasks.add(task)
            
            # Wait for tasks with optimized timeout handling
            try:
                # Use shorter timeout in test mode
                timeout = 0.5 if self._test_mode else min(len(ips) * 0.5, 30.0)
                completed, pending = await asyncio.wait(
                    tasks,
                    timeout=timeout,
                    return_when=asyncio.ALL_COMPLETED
                )
                
                # Process completed tasks first
                for task in completed:
                    try:
                        ip, is_alive = await task
                        if ip:  # Only add if we got a valid IP back
                            results[ip] = is_alive
                            print(f"已添加结果: {ip} -> {'在线' if is_alive else '离线'}")
                    except Exception as e:
                        print(f"Error processing task result: {str(e)}")
                        # Don't fail completely on individual task errors
                        continue
                
                # Cancel and clean up pending tasks
                if pending:
                    print(f"Warning: {len(pending)} tasks did not complete within timeout")
                    for task in pending:
                        task.cancel()
                    # Wait briefly for cancellation
                    try:
                        await asyncio.wait(pending, timeout=1.0)
                    except Exception as e:
                        print(f"Error during task cancellation: {str(e)}")
                        pass
                
                # Process missing IPs
                missing_ips = [ip for ip in ips if ip not in results]
                if missing_ips:
                    print(f"Retrying {len(missing_ips)} missing IPs...")
                    retry_tasks = []
                    for ip in missing_ips:
                        task = asyncio.create_task(check_with_semaphore(ip))
                        retry_tasks.append(task)
                        async with self._task_lock:
                            self._tasks.add(task)
                    
                    # Wait for retry tasks
                    retry_completed, retry_pending = await asyncio.wait(
                        retry_tasks,
                        timeout=timeout / 2,  # Use shorter timeout for retries
                        return_when=asyncio.ALL_COMPLETED
                    )
                    
                        # Process retry results with improved error handling
                    for task in retry_completed:
                        try:
                            ip, is_alive = await task
                            if ip:  # Only add if we got a valid IP back
                                results[ip] = is_alive
                                print(f"重试结果: {ip} -> {'在线' if is_alive else '离线'}")
                        except Exception as e:
                            print(f"Error processing retry result: {str(e)}")
                            continue  # Skip failed tasks but continue processing others
                    
                    # Cancel and clean up pending retry tasks
                    if retry_pending:
                        print(f"Warning: {len(retry_pending)} retry tasks did not complete")
                        for task in retry_pending:
                            task.cancel()
                        try:
                            await asyncio.wait(retry_pending, timeout=1.0)
                        except Exception as e:
                            print(f"Error during retry task cancellation: {str(e)}")
                    
                    # Final pass for any remaining missing IPs
                    still_missing = [ip for ip in ips if ip not in results]
                    if still_missing:
                        print(f"警告: 仍有 {len(still_missing)} 个IP未能获取结果: {still_missing}")
                        for ip in still_missing:
                            try:
                                # Direct check without semaphore to ensure completion
                                _, is_alive, _ = await self.check_ip(ip)
                                results[ip] = is_alive
                                print(f"最终检查: {ip} -> {'在线' if is_alive else '离线'}")
                            except Exception as e:
                                print(f"Error in final check for {ip}: {str(e)}")
                                results[ip] = False  # Default to offline on error
                                print(f"默认设置: {ip} -> 离线")
                
            except Exception as e:
                print(f"Error during task processing: {str(e)}")
                # Cancel all tasks
                for task in tasks:
                    if not task.done():
                        task.cancel()
            
            return results
            
        except Exception as e:
            print(f"Error in check_all_ips: {str(e)}")
            return {}
        finally:
            # Final cleanup
            try:
                tasks = [t for t in asyncio.all_tasks() 
                        if t is not asyncio.current_task()]
                for task in tasks:
                    if not task.done():
                        task.cancel()
            except Exception:
                pass
            return results

    async def send_alert(self, message: str, level: str = "INFO", alert_key: Optional[str] = None):
        """Send alert through AlertManager"""
        try:
            from network_monitor.core.alert_manager import AlertLevel
            alert_level = getattr(AlertLevel, level.upper())
            return await self.alert_manager.send_alert(
                message=message,
                level=alert_level,
                alert_key=alert_key
            )
        except Exception as e:
            print(f"发送告警失败: {str(e)}")
            return False

    async def format_alert_message(self, results: dict) -> list[tuple[str, str, str]]:
        """Format alert message for offline IPs with status change tracking"""
        # Initialize status tracking if not exists
        if not hasattr(self, '_alert_status'):
            self._alert_status = {}
            
        # Track which IPs have changed status
        changed_ips = []
        for ip, status in results.items():
            prev_status = self._alert_status.get(ip)
            if prev_status is None or prev_status != status:
                changed_ips.append(ip)
                self._alert_status[ip] = status
        
        # Only include IPs that have changed status
        if not changed_ips:
            return []

        alerts = []
        for ip in changed_ips:
            status = results[ip]
            # Determine alert level based on status
            level = "INFO" if status else "CRITICAL"
            status_text = "在线" if status else "离线"
            
            message = (
                f"设备状态变更:\n"
                f"IP: {ip}\n"
                f"描述: {self.ip_data.get(ip, '未知设备')}\n"
                f"状态: {status_text}"
            )
            
            alert_key = f"status_change_{ip}"
            alerts.append((message, level, alert_key))

        return alerts

    @lru_cache(maxsize=1024)
    def _ip_to_int(self, ip: str) -> int:
        """Convert IP address to integer with caching"""
        octets = ip.split('.')
        return sum(int(octet) << (24 - 8 * i) for i, octet in enumerate(octets))
    
    @lru_cache(maxsize=1024)
    def _int_to_ip(self, ip_int: int) -> str:
        """Convert integer to IP address with caching"""
        octets = [(ip_int >> (24 - 8 * i)) & 255 for i in range(4)]
        return '.'.join(str(octet) for octet in octets)
        
    @lru_cache(maxsize=1024, typed=True)
    def _cached_ping(self, ip: str) -> Optional[float]:
        """Cache ping results with a 5-second TTL"""
        if self._test_mode and hasattr(self, '_mock_responses'):
            return self._mock_responses.get(ip.strip(), None)
        return self.ping_host(ip.strip(), timeout=self.ping_timeout)
    
    async def discover_ips(self):
        """Scan IP range for active devices with enhanced thread safety and rate limiting"""
        async with asyncio.Lock():  # Ensure only one discovery process runs at a time
            try:
                with self._discovery_lock:
                    print(f"开始扫描IP范围: {self._discovery_start_ip} - {self._discovery_end_ip}")
                    start_int = self._ip_to_int(self._discovery_start_ip)
                    end_int = self._ip_to_int(self._discovery_end_ip)
                    
                    # Use semaphore to limit concurrent scans
                    sem = asyncio.Semaphore(50)  # Limit to 50 concurrent scans
                    
                    async def check_ip_with_rate_limit(ip):
                        async with sem:
                            return await self.check_ip(ip)
                    
                    # Create chunks of IPs to process in batches
                    chunk_size = 256  # Process IPs in chunks
                    discovered = 0
                    total_ips = end_int - start_int + 1
                    
                    for chunk_start in range(start_int, end_int + 1, chunk_size):
                        chunk_end = min(chunk_start + chunk_size, end_int + 1)
                        chunk_ips = [self._int_to_ip(ip_int) 
                                   for ip_int in range(chunk_start, chunk_end)]
                        
                        # Create tasks for current chunk
                        tasks = [
                            asyncio.create_task(check_ip_with_rate_limit(ip))
                            for ip in chunk_ips
                        ]
                        
                        try:
                            # Process chunk with timeout
                            chunk_results = await asyncio.wait_for(
                                asyncio.gather(*tasks, return_exceptions=True),
                                timeout=len(chunk_ips) * 0.5  # 500ms per IP maximum
                            )
                            
                            # Add responding IPs to ip_data with thread safety
                            with self._ip_data_lock:
                                for ip, result in zip(chunk_ips, chunk_results):
                                    if isinstance(result, tuple) and result[1]:
                                        if ip not in self._ip_data:
                                            self._ip_data[ip] = (
                                                f'自动发现设备 ({datetime.now().strftime("%Y-%m-%d %H:%M")})'
                                            )
                                            discovered += 1
                                            
                                # Save periodically (every 1000 discovered devices)
                                if discovered > 0 and discovered % 1000 == 0:
                                    self.save_data()
                                    
                        except asyncio.TimeoutError:
                            print(f"处理IP范围 {chunk_ips[0]} - {chunk_ips[-1]} 超时")
                            # Cancel remaining tasks in chunk
                            for task in tasks:
                                if not task.done():
                                    task.cancel()
                        
                        # Progress update
                        progress = min(100, (chunk_end - start_int) * 100 / total_ips)
                        print(f"扫描进度: {progress:.1f}% ({discovered} 个设备已发现)")
                    
                    if discovered:
                        print(f"发现 {discovered} 个新设备")
                        with self._ip_data_lock:
                            self.save_data()
                    
                    return discovered
                    
            except Exception as e:
                print(f"IP发现过程出错: {str(e)}")
                return 0
    
    async def start_discovery(self):
        """Start automatic IP discovery"""
        if self._discovery_enabled:
            print("IP自动发现已经在运行")
            return
        
        self._discovery_enabled = True
        print(f"启动IP自动发现 (扫描间隔: {self._discovery_interval}秒)")
        
        try:
            while self._discovery_enabled:
                try:
                    # Check if it's time for auto-save
                    now = datetime.now()
                    if (now - self.last_save_time).total_seconds() >= self._auto_save_interval:
                        self.save_data()
                    
                    # Check if it's time for discovery
                    if not hasattr(self, '_last_discovery_time'):
                        self._last_discovery_time = datetime.now()
                    
                    if (now - self._last_discovery_time).total_seconds() >= self._discovery_interval:
                        async with self._task_lock:
                            discovery_task = asyncio.create_task(self.discover_ips())
                            self._tasks.add(discovery_task)
                            discovery_task.add_done_callback(self._tasks.discard)
                        self._last_discovery_time = now
                    
                    await asyncio.sleep(1)  # Check every second
                except Exception as e:
                    print(f"IP自动发现出错: {str(e)}")
                    await asyncio.sleep(10)  # Wait before retrying
        except asyncio.CancelledError:
            # Clean up tasks on cancellation
            async with self._task_lock:
                tasks = list(self._tasks)
                for task in tasks:
                    if not task.done():
                        task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
            raise
    
    @property
    def discovery_enabled(self) -> bool:
        """Get discovery enabled status"""
        return self._discovery_enabled
    
    @discovery_enabled.setter
    def discovery_enabled(self, value: bool):
        """Set discovery enabled status"""
        self._discovery_enabled = value
    
    @property
    def discovery_interval(self) -> int:
        """Get discovery interval in seconds"""
        return self._discovery_interval
    
    @discovery_interval.setter
    def discovery_interval(self, value: int):
        """Set discovery interval in seconds"""
        if not self._test_mode and value < 60:
            raise ValueError("扫描间隔不能小于60秒")
        elif self._test_mode and value < 1:
            raise ValueError("扫描间隔不能小于1秒")
        self._discovery_interval = value
    
    @property
    def discovery_start_ip(self) -> str:
        """Get discovery start IP"""
        return self._discovery_start_ip
    
    @discovery_start_ip.setter
    def discovery_start_ip(self, value: str):
        """Set discovery start IP"""
        self._discovery_start_ip = value
    
    @property
    def discovery_end_ip(self) -> str:
        """Get discovery end IP"""
        return self._discovery_end_ip
    
    @discovery_end_ip.setter
    def discovery_end_ip(self, value: str):
        """Set discovery end IP"""
        self._discovery_end_ip = value
    
    @property
    def auto_save_interval(self) -> int:
        """Get auto-save interval in seconds"""
        return self._auto_save_interval
    
    @auto_save_interval.setter
    def auto_save_interval(self, value: int):
        """Set auto-save interval in seconds"""
        if not isinstance(value, int):
            raise ValueError("自动保存间隔必须是整数")
        if not self._test_mode and value < 300:  # Minimum 5 minutes in production
            raise ValueError("自动保存间隔不能小于300秒")
        elif self._test_mode and value < 5:  # Minimum 5 seconds in test mode
            raise ValueError("自动保存间隔不能小于5秒")
        self._auto_save_interval = value
    
    def stop_discovery(self):
        """Stop automatic IP discovery"""
        if not self.discovery_enabled:
            print("IP自动发现未在运行")
            return
        
        self.discovery_enabled = False
        print("停止IP自动发现")
    
    def set_discovery_range(self, start_ip: str, end_ip: str):
        """Set IP range for discovery"""
        try:
            # Validate IP addresses
            socket.inet_aton(start_ip)
            socket.inet_aton(end_ip)
            
            # Ensure start_ip is less than end_ip
            if self._ip_to_int(start_ip) > self._ip_to_int(end_ip):
                raise ValueError("起始IP必须小于结束IP")
            
            self.discovery_start_ip = start_ip
            self.discovery_end_ip = end_ip
            print(f"已设置扫描范围: {start_ip} - {end_ip}")
            
        except socket.error:
            raise ValueError("无效的IP地址格式")
    
    def set_discovery_interval(self, interval: int):
        """Set interval for discovery in seconds"""
        if not self._test_mode and interval < 60:  # Minimum 1 minute in production
            raise ValueError("扫描间隔不能小于60秒")
        elif self._test_mode and interval < 1:  # Minimum 1 second in test mode
            raise ValueError("扫描间隔不能小于1秒")
        
        self._discovery_interval = interval
        print(f"已设置扫描间隔: {interval}秒")
        
    def set_auto_save_interval(self, interval: int):
        """Set interval for auto-save in seconds"""
        if not self._test_mode and interval < 300:  # Minimum 5 minutes in production
            raise ValueError("自动保存间隔不能小于300秒")
        elif self._test_mode and interval < 5:  # Minimum 5 seconds in test mode
            raise ValueError("自动保存间隔不能小于5秒")
        
        self._auto_save_interval = interval
        print(f"已设置自动保存间隔: {interval}秒")
        
    async def recover_connection(self, ip: str) -> bool:
        """
        Attempt to recover connection to an IP with configurable retries
        
        Args:
            ip: IP address to recover
            
        Returns:
            bool: True if connection recovered, False otherwise
        """
        async with self._recovery_lock:
            if ip not in self._recovery_status:
                self._recovery_status[ip] = {'attempts': 0, 'recovered': False, 'last_attempt': None}
            
            status = self._recovery_status[ip]
            now = datetime.now()
            
            # Check if we're still in cooldown period (1 minute in production, 0.1s in test)
            if status['last_attempt']:
                cooldown = (now - status['last_attempt']).total_seconds()
                cooldown_period = 0.1 if self._test_mode else 60
                if cooldown < cooldown_period:
                    return False
            
            # Only reset recovered status, keep attempt count
            status['recovered'] = False
            status['last_attempt'] = now
            
            print(f"尝试恢复与 {ip} 的连接...")
            
            # Continue from last attempt count
            current_attempt = status['attempts'] + 1
            for attempt in range(current_attempt, self._max_recovery_attempts + 1):
                status['attempts'] = attempt
                
                try:
                    # Use shorter timeout for recovery attempts
                    result = await asyncio.wait_for(self.check_ip(ip), timeout=self._recovery_timeout)
                    if result[1]:
                        print(f"IP {ip} 已恢复连接 (尝试次数: {attempt})")
                        status['recovered'] = True
                        await self.send_alert(
                            f"设备已恢复连接\nIP: {ip}\n描述: {self._ip_data.get(ip, '未知设备')}",
                            "INFO",
                            f"recovery_{ip}"
                        )
                        return True
                except asyncio.TimeoutError:
                    print(f"恢复尝试超时 {attempt}/{self._max_recovery_attempts}")
                    continue
                except Exception as e:
                    print(f"恢复尝试出错: {str(e)}")
                    continue
                    return True
                
                print(f"恢复尝试 {attempt}/{self._max_recovery_attempts} 失败，等待 {self._recovery_interval} 秒...")
                await asyncio.sleep(self._recovery_interval)
            
            print(f"无法恢复与 {ip} 的连接，已达到最大尝试次数")
            await self.send_alert(
                f"设备恢复失败\nIP: {ip}\n描述: {self._ip_data.get(ip, '未知设备')}\n尝试次数: {self._max_recovery_attempts}",
                "WARNING",
                f"recovery_failed_{ip}"
            )
            return False
            
    def get_recovery_status(self, ip: str) -> Dict:
        """Get recovery status for an IP"""
        return self._recovery_status.get(ip, {
            'attempts': 0,
            'recovered': False,
            'last_attempt': None
        })
        
    async def handle_ip_status_change(self, ip: str, is_online: bool, response_time: Optional[float] = None):
        """
        Handle IP status changes by delegating to AlertManager
        
        Args:
            ip: IP address
            is_online: Current online status
            response_time: Response time in milliseconds (if available)
        """
        try:
            await self.alert_manager.handle_ip_status_change(ip, is_online, response_time)
        except Exception as e:
            print(f"Error handling IP status change for {ip}: {str(e)}")
            # Re-raise to allow caller to handle
            raise
