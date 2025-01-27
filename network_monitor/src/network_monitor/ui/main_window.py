from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QLabel, QLineEdit, QMessageBox, QHeaderView,
                            QTabWidget, QSpinBox, QComboBox, QTextEdit,
                            QGroupBox, QInputDialog, QScrollArea, QFrame,
                            QSplitter)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsOpacityEffect
import asyncio
import json
import socket
import sys
import threading
import time
from typing import Dict, List, Optional
from functools import partial
import os

from network_monitor.core.network_monitor import NetworkMonitor
from .animation_manager import AnimationManager
from .sound_manager import SoundManager

class MainWindow(QMainWindow):
    def __init__(self, security_manager):
        super().__init__()
        print("正在初始化网络监控系统...")
        self.security_manager = security_manager
        self.session_token = None
        
        # Initialize notification tracking
        self._ip_status_history = {}  # Track IP status changes
        self._notification_history = {}  # Track notification timestamps
        self._message_history = {}  # Track message frequency
        self._notification_cooldown = 300  # 5 minutes cooldown
        
        # Show login dialog
        self.show_login()
        
        # Only initialize if logged in
        if self.session_token:
            self.monitor = NetworkMonitor()
            self._event_loop = asyncio.new_event_loop()
            self._event_loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self._event_loop_thread.start()
            self.animation_manager = AnimationManager()
            self.sound_manager = SoundManager()
            self.init_ui()
            self.setup_refresh_timer()
            self.storm_detection_timer = QTimer()
            self.storm_detection_timer.timeout.connect(self.check_network_storm)
            self.storm_detection_timer.start(5000)  # Check every 5 seconds
            print("网络监控系统初始化完成")
        else:
            self.close()
    
    def show_login(self):
        """Show login dialog and handle authentication"""
        from .login_dialog import LoginDialog
        dialog = LoginDialog(self.security_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.session_token = dialog.get_session_token()
            self.update_title()
        
    def update_title(self):
        """Update window title with user role"""
        role = self.security_manager.get_user_role(self.session_token)
        self.setWindowTitle(f"网络监控系统 - {role.upper()}")
        
    def update_button_visibility(self):
        """Update button visibility based on user permissions"""
        # Get current permissions
        can_export = self.security_manager.has_permission(self.session_token, 'export_data')
        can_edit = self.security_manager.has_permission(self.session_token, 'edit_ip')
        is_admin = self.security_manager.has_permission(self.session_token, 'all')
        
        # Update button states
        self.export_btn.setEnabled(can_export)
        if hasattr(self, 'port_input'):
            self.port_input.setEnabled(can_edit)
        if hasattr(self, 'ip_input'):
            self.ip_input.setEnabled(can_edit)
            self.desc_input.setEnabled(can_edit)
        
        # Update table buttons
        for row in range(self.ip_table.rowCount()):
            delete_btn = self.ip_table.cellWidget(row, 4)
            if delete_btn:
                delete_btn.setEnabled(is_admin)
        
        # Update backup buttons if they exist
        if hasattr(self, 'backup_list'):
            for row in range(self.backup_list.rowCount()):
                restore_btn = self.backup_list.cellWidget(row, 2)
                if restore_btn:
                    restore_btn.setEnabled(is_admin)
    
    def logout(self):
        """Handle user logout"""
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出登录吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Invalidate session
            if self.session_token:
                self.security_manager.logout(self.session_token)
                self.session_token = None
            
            # Show login dialog
            self.show_login()
            
            # If login failed, close the application
            if not self.session_token:
                self.close()
            else:
                # Refresh UI with new permissions
                self.update_title()
                self.update_button_visibility()
                self.log_message("用户已重新登录", "info")
        
    def _run_event_loop(self):
        """Run the event loop in a background thread"""
        asyncio.set_event_loop(self._event_loop)
        self._event_loop.run_forever()
        
    def closeEvent(self, event):
        """Clean up resources when the window is closed"""
        if self._event_loop is not None:
            self._event_loop.call_soon_threadsafe(self._event_loop.stop)
            self._event_loop_thread.join()
        super().closeEvent(event)

    def init_ui(self):
        self.setWindowTitle('矿井网络监控系统')
        self.setMinimumSize(1024, 768)
        
        # Start session check timer
        self.session_check_timer = QTimer()
        self.session_check_timer.timeout.connect(self.check_session)
        self.session_check_timer.start(60000)  # Check every minute

        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # IP Monitor Tab
        ip_monitor_tab = QWidget()
        ip_layout = QVBoxLayout(ip_monitor_tab)
        
        # Add IP input section
        input_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('输入IP地址')
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText('输入描述')
        add_btn = QPushButton('添加')
        add_btn.clicked.connect(self.add_ip)
        
        input_layout.addWidget(QLabel('IP:'))
        input_layout.addWidget(self.ip_input)
        input_layout.addWidget(QLabel('描述:'))
        input_layout.addWidget(self.desc_input)
        input_layout.addWidget(add_btn)
        ip_layout.addLayout(input_layout)
        
        # Port Monitor Section
        port_layout = QHBoxLayout()
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(80)
        add_port_btn = QPushButton('添加端口监控')
        add_port_btn.clicked.connect(self.add_port_monitor)
        
        port_layout.addWidget(QLabel('端口:'))
        port_layout.addWidget(self.port_input)
        port_layout.addWidget(add_port_btn)
        ip_layout.addLayout(port_layout)
        
        # IP Discovery Section
        discovery_group = QGroupBox("IP自动发现")
        discovery_layout = QVBoxLayout()
        
        # Discovery control buttons
        discovery_buttons = QHBoxLayout()
        self.start_discovery_button = QPushButton("启动自动发现")
        self.start_discovery_button.clicked.connect(
            lambda: asyncio.run_coroutine_threadsafe(self.start_discovery(), self._event_loop)
        )
        discovery_buttons.addWidget(self.start_discovery_button)
        
        self.stop_discovery_button = QPushButton("停止自动发现")
        self.stop_discovery_button.clicked.connect(self.stop_discovery)
        self.stop_discovery_button.setEnabled(False)
        discovery_buttons.addWidget(self.stop_discovery_button)
        discovery_layout.addLayout(discovery_buttons)
        
        # Discovery range settings
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("扫描范围:"))
        self.start_ip_edit = QLineEdit("10.246.65.1")
        range_layout.addWidget(self.start_ip_edit)
        range_layout.addWidget(QLabel("到"))
        self.end_ip_edit = QLineEdit("10.246.81.254")
        range_layout.addWidget(self.end_ip_edit)
        set_range_button = QPushButton("设置范围")
        set_range_button.clicked.connect(self.set_discovery_range)
        range_layout.addWidget(set_range_button)
        discovery_layout.addLayout(range_layout)
        
        # Discovery interval settings
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("扫描间隔(分钟):"))
        self.interval_edit = QSpinBox()
        self.interval_edit.setRange(1, 60)  # 1 minute to 1 hour
        self.interval_edit.setValue(5)  # Default 5 minutes
        interval_layout.addWidget(self.interval_edit)
        set_interval_button = QPushButton("设置间隔")
        set_interval_button.clicked.connect(self.set_discovery_interval)
        interval_layout.addWidget(set_interval_button)
        discovery_layout.addLayout(interval_layout)
        
        discovery_group.setLayout(discovery_layout)
        ip_layout.addWidget(discovery_group)
        
        # Add IP monitoring table
        self.ip_table = QTableWidget()
        self.ip_table.setColumnCount(5)
        self.ip_table.setHorizontalHeaderLabels(['IP地址', '描述', '状态', '端口状态', '操作'])
        self.ip_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        ip_layout.addWidget(self.ip_table)

        # Add control buttons for IP monitoring
        ip_btn_layout = QHBoxLayout()
        
        # Refresh button (always visible)
        refresh_btn = QPushButton('刷新状态')
        refresh_btn.clicked.connect(self.refresh_status)
        ip_btn_layout.addWidget(refresh_btn)
        
        # Import/Export buttons (viewer or higher)
        self.import_btn = QPushButton('导入数据')
        self.import_btn.clicked.connect(self.import_data)
        ip_btn_layout.addWidget(self.import_btn)
        
        self.export_btn = QPushButton('导出数据')
        self.export_btn.clicked.connect(self.export_data)
        ip_btn_layout.addWidget(self.export_btn)
        
        self.batch_modify_btn = QPushButton('批量修改描述')
        self.batch_modify_btn.clicked.connect(self.batch_modify_descriptions)
        ip_btn_layout.addWidget(self.batch_modify_btn)
        
        # Logout button
        logout_btn = QPushButton('退出登录')
        logout_btn.clicked.connect(self.logout)
        ip_btn_layout.addWidget(logout_btn)
        
        ip_layout.addLayout(ip_btn_layout)
        
        # Update button visibility based on permissions
        self.update_button_visibility()

        # Network Statistics Tab
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        
        # Interface Selection
        iface_layout = QHBoxLayout()
        self.iface_combo = QComboBox()
        self.update_interface_list()
        iface_layout.addWidget(QLabel('网络接口:'))
        iface_layout.addWidget(self.iface_combo)
        stats_layout.addLayout(iface_layout)
        
        # Network Usage Display
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        
        # Storm Detection Status
        self.storm_status = QLabel('网络风暴状态: 正常')
        stats_layout.addWidget(self.storm_status)
        
        # System Log Tab
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        
        # Log filter section
        filter_frame = QGroupBox("日志过滤")
        filter_layout = QHBoxLayout()
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(['全部', '信息', '警告', '错误'])
        self.log_level_combo.currentTextChanged.connect(self.filter_logs)
        
        self.log_search = QLineEdit()
        self.log_search.setPlaceholderText('搜索日志...')
        self.log_search.textChanged.connect(self.filter_logs)
        
        clear_log_btn = QPushButton('清除日志')
        clear_log_btn.clicked.connect(self.clear_logs)
        
        filter_layout.addWidget(QLabel('日志级别:'))
        filter_layout.addWidget(self.log_level_combo)
        filter_layout.addWidget(QLabel('搜索:'))
        filter_layout.addWidget(self.log_search)
        filter_layout.addWidget(clear_log_btn)
        filter_frame.setLayout(filter_layout)
        log_layout.addWidget(filter_frame)
        
        # Log display
        log_display_frame = QGroupBox("系统日志")
        log_display_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                font-family: monospace;
            }
        """)
        log_display_layout.addWidget(self.log_text)
        log_display_frame.setLayout(log_display_layout)
        log_layout.addWidget(log_display_frame)
        
        # Backup Management Tab
        backup_tab = QWidget()
        backup_layout = QVBoxLayout(backup_tab)
        
        # Backup controls
        backup_controls = QHBoxLayout()
        force_backup_btn = QPushButton('创建备份')
        force_backup_btn.clicked.connect(lambda: self.monitor.save_data(force=True))
        
        restore_backup_btn = QPushButton('恢复备份')
        restore_backup_btn.clicked.connect(self.restore_backup)
        
        backup_controls.addWidget(force_backup_btn)
        backup_controls.addWidget(restore_backup_btn)
        backup_layout.addLayout(backup_controls)
        
        # Backup list
        self.backup_list = QTableWidget()
        self.backup_list.setColumnCount(3)
        self.backup_list.setHorizontalHeaderLabels(['备份时间', '文件名', '操作'])
        self.backup_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.backup_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        backup_layout.addWidget(self.backup_list)
        
        # Add all tabs
        tabs.addTab(ip_monitor_tab, "IP监控")
        tabs.addTab(stats_tab, "网络统计")
        tabs.addTab(log_tab, "系统日志")
        tabs.addTab(backup_tab, "备份管理")
        
        # Initialize logging system
        self.log_message("系统启动", "info")
        self.log_message("开始监控网络设备", "info")
        
        # Set up auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(lambda: self.monitor.save_data())
        self.auto_save_timer.start(1200000)  # 20 minutes
        self.log_message("自动保存已启用 (间隔: 20分钟)", "info")

    def setup_refresh_timer(self):
        """Set up automatic refresh timers"""
        print("设置定时刷新...")
        
        # Create a background event loop for async operations
        self._event_loop = asyncio.new_event_loop()
        self._event_loop_thread = threading.Thread(
            target=self._run_event_loop,
            daemon=True
        )
        self._event_loop_thread.start()
        
        # Initial refresh using the background event loop
        asyncio.run_coroutine_threadsafe(self.refresh_table(), self._event_loop)
        asyncio.run_coroutine_threadsafe(self.refresh_status(), self._event_loop)
        
        # IP status refresh timer (every 30 seconds for testing)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(
            lambda: asyncio.run_coroutine_threadsafe(
                self.refresh_status(), self._event_loop
            )
        )
        self.refresh_timer.start(30000)
        print("IP状态刷新定时器已启动 (间隔: 30秒)")

        # Network statistics refresh timer (every 5 seconds)
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_network_stats)
        self.stats_timer.start(5000)
        print("网络统计刷新定时器已启动 (间隔: 5秒)")
        
        # Backup list refresh timer (every minute)
        self.backup_refresh_timer = QTimer()
        self.backup_refresh_timer.timeout.connect(self.refresh_backup_list)
        self.backup_refresh_timer.start(60000)  # 1 minute
        self.refresh_backup_list()  # Initial refresh
        print("备份列表刷新定时器已启动 (间隔: 1分钟)")

    def add_ip(self):
        """Add new IP to monitoring"""
        if not self.security_manager.has_permission(self.session_token, 'add_ip'):
            self.log_message('添加IP失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '您没有添加IP的权限')
            return
            
        ip = self.ip_input.text().strip()
        desc = self.desc_input.text().strip()
        
        if not ip or not desc:
            self.log_message('添加IP失败：IP和描述不能为空', 'error')
            QMessageBox.warning(self, '输入错误', 'IP和描述不能为空')
            return

        # Validate IP address format
        try:
            socket.inet_aton(ip)
        except socket.error:
            self.log_message(f'添加IP失败：{ip} 格式无效', 'error')
            QMessageBox.warning(self, '输入错误', 'IP地址格式无效')
            return

        self.monitor.add_ip(ip, desc)
        self.monitor.save_data()  # Save to persistent storage
        self.log_message(f'添加IP成功：{ip} ({desc})', 'success')
        
        # Schedule async refresh in the background event loop
        asyncio.run_coroutine_threadsafe(self.refresh_table(), self._event_loop)
        
        self.ip_input.clear()
        self.desc_input.clear()

    def remove_ip(self, ip: str):
        """Remove IP from monitoring"""
        if not self.security_manager.has_permission(self.session_token, 'all'):
            self.log_message('移除IP失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '只有管理员可以删除IP')
            return
            
        try:
            desc = self.monitor.get_all_ips().get(ip, '未知设备')
            self.monitor.remove_ip(ip)
            self.monitor.save_data()  # Save changes to persistent storage
            self.log_message(f'移除IP成功：{ip} ({desc})', 'info')
        except Exception as e:
            self.log_message(f'移除IP失败：{ip} - {str(e)}', 'error')
        
        # Schedule async refresh in the background event loop
        asyncio.run_coroutine_threadsafe(self.refresh_table(), self._event_loop)

    async def refresh_table(self):
        """Refresh the IP table display"""
        print("刷新IP表格...")
        self.ip_table.setRowCount(0)
        for row, (ip, desc) in enumerate(self.monitor.get_all_ips().items()):
            self.ip_table.insertRow(row)
            self.ip_table.setItem(row, 0, QTableWidgetItem(ip))
            self.ip_table.setItem(row, 1, QTableWidgetItem(desc))
            self.ip_table.setItem(row, 2, QTableWidgetItem('检查中...'))
            
            # Port status column
            port_status = []
            try:
                for port in self.monitor.monitored_ports:
                    try:
                        is_open = await self.monitor.check_port(ip, port)
                        port_status.append(f"{port}: {'开放' if is_open else '关闭'}")
                    except Exception as e:
                        print(f"检查端口 {ip}:{port} 时出错: {str(e)}")
                        port_status.append(f"{port}: 错误")
            except Exception as e:
                print(f"处理IP {ip} 的端口状态时出错: {str(e)}")
                port_status.append("端口检查出错")
            
            port_status_item = QTableWidgetItem('\n'.join(port_status) if port_status else '无监控端口')
            self.ip_table.setItem(row, 3, port_status_item)
            
            delete_btn = QPushButton('删除')
            delete_btn.clicked.connect(lambda ip=ip: self.remove_ip(ip))
            self.ip_table.setCellWidget(row, 4, delete_btn)
        print("IP表格刷新完成")

    async def refresh_status(self):
        """Refresh status of monitored IPs"""
        print("\n开始刷新IP状态...")
        try:
            # Only check monitored IPs if monitoring is active
            if not self.monitoring_active:
                print("监控未启动")
                return
                
            # Get status for monitored IPs only
            results = {}
            for ip in self.monitored_ips:
                status = await self.monitor.check_ip(ip)
                results[ip] = status
                
            print(f"检查完成，共 {len(results)} 个IP")
            online_count = sum(1 for status in results.values() if status)
            offline_count = len(results) - online_count
            print(f"在线: {online_count}, 离线: {offline_count}")
            
            for row in range(self.ip_table.rowCount()):
                ip = self.ip_table.item(row, 0).text()
                if ip in self.monitored_ips:
                    status = results.get(ip, False)
                    status_text = '在线' if status else '离线'
                    status_item = QTableWidgetItem(status_text)
                    status_item.setForeground(Qt.GlobalColor.green if status else Qt.GlobalColor.red)
                else:
                    status_text = '未监控'
                    status_item = QTableWidgetItem(status_text)
                    status_item.setForeground(Qt.GlobalColor.gray)
                self.ip_table.setItem(row, 2, status_item)
                
                # Animate status change
                self.animation_manager.fade_in(self.ip_table.cellWidget(row, 2) or self.ip_table.item(row, 2))
                
                # Flash red background and play sound for offline monitored devices
                if ip in self.monitored_ips:
                    if not status:
                        # Check if status has changed before triggering notifications
                        prev_status = self._ip_status_history.get(ip)
                        if prev_status is None or prev_status != status:
                            self._ip_status_history[ip] = status
                            current_time = time.time()
                            notification_key = f"offline_{ip}"
                            last_notification = self._notification_history.get(notification_key, 0)
                            
                            if current_time - last_notification > self._notification_cooldown:
                                self.animation_manager.flash_status(
                                    self.ip_table.cellWidget(row, 2) or self.ip_table.item(row, 2),
                                    QColor(255, 200, 200)  # Light red
                                )
                                self.sound_manager.play_sound('device_offline')
                                self.log_message(f"设备离线: {ip}", "warning")
                                self._notification_history[notification_key] = current_time
                    print(f"IP: {ip} - {status_text}")

                    # Update port status for monitored IPs
                    port_status = []
                    try:
                        port_check_tasks = [
                            self.monitor.check_port(ip, port) 
                            for port in self.monitor.monitored_ports
                        ]
                        port_results = await asyncio.gather(*port_check_tasks)
                        
                        for port, is_open in zip(self.monitor.monitored_ports, port_results):
                            port_status.append(f"{port}: {'开放' if is_open else '关闭'}")
                    except Exception as e:
                        print(f"检查IP {ip} 的端口时出错: {str(e)}")
                        port_status.append("端口检查出错")
                else:
                    port_status = ['未监控']
                
                port_status_item = QTableWidgetItem('\n'.join(port_status))
                self.ip_table.setItem(row, 3, port_status_item)

            # Only send alerts for offline monitored IPs
            offline_ips = {ip: desc for ip, desc in self.monitor.get_all_ips().items() 
                         if ip in self.monitored_ips and not results.get(ip, False)}
            if offline_ips:
                messages = self.monitor.format_alert_message({ip: False for ip in offline_ips})
                for message in messages:
                    self.monitor.send_wechat_alert(message)

            # Update network statistics and check storm conditions
            self.update_network_stats()
            self.check_network_storm()
            
        except Exception as e:
            print(f"刷新状态时出错: {str(e)}")
            # Set error status in the UI for monitored IPs
            for row in range(self.ip_table.rowCount()):
                ip = self.ip_table.item(row, 0).text()
                if ip in self.monitored_ips:
                    self.ip_table.setItem(row, 2, QTableWidgetItem('错误'))
                    self.ip_table.setItem(row, 3, QTableWidgetItem('检查出错'))

    def update_interface_list(self):
        """Update network interface list in combo box"""
        self.iface_combo.clear()
        interfaces = self.monitor.get_network_interfaces()
        
        # Add interfaces with detailed information
        for iface in interfaces:
            # Format interface information
            name = iface['name']
            ip = iface.get('ip', 'N/A')
            mac = iface.get('mac', 'N/A')
            status = iface.get('status', '未知')
            speed = iface.get('speed', 0)
            
            # Create a detailed display string
            display_text = f"{name} - {status}"
            if ip != 'N/A':
                display_text += f"\nIP: {ip}"
            if mac != 'N/A':
                display_text += f"\nMAC: {mac}"
            if speed > 0:
                display_text += f"\n速率: {speed} Mbps"
            
            # Add to combo box with full data as tooltip
            self.iface_combo.addItem(display_text)
            last_idx = self.iface_combo.count() - 1
            self.iface_combo.setItemData(last_idx, 
                                       f"接口详细信息:\n{display_text}", 
                                       Qt.ItemDataRole.ToolTipRole)
            
            # Set different background colors based on status
            if status == '在线':
                self.iface_combo.setItemData(last_idx, 
                                           QColor(200, 255, 200), 
                                           Qt.ItemDataRole.BackgroundRole)
            elif status == '离线':
                self.iface_combo.setItemData(last_idx, 
                                           QColor(255, 200, 200), 
                                           Qt.ItemDataRole.BackgroundRole)
        
        # Add refresh button next to combo box if not already added
        if not hasattr(self, 'refresh_iface_btn'):
            self.refresh_iface_btn = QPushButton('刷新接口列表')
            self.refresh_iface_btn.clicked.connect(self.update_interface_list)
            # Find the interface layout
            for i in range(self.centralWidget().layout().count()):
                widget = self.centralWidget().layout().itemAt(i).widget()
                if isinstance(widget, QTabWidget):
                    for j in range(widget.count()):
                        if widget.tabText(j) == "网络统计":
                            tab = widget.widget(j)
                            for child in tab.children():
                                if isinstance(child, QHBoxLayout) and \
                                   any(isinstance(w, QComboBox) for w in child.children()):
                                    child.addWidget(self.refresh_iface_btn)
                                    break
        
        # Log interface update
        print(f"更新网络接口列表: 发现 {len(interfaces)} 个接口")
        for iface in interfaces:
            print(f"- {iface['name']}: {iface.get('ip', 'N/A')} ({iface.get('status', '未知')})")

    def add_port_monitor(self):
        """Add port to monitoring list with validation and detailed status"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            self.log_message('添加端口监控失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '您没有添加端口监控的权限')
            return
            
        port = self.port_input.value()
        
        # Validate port number
        if port in self.monitor.monitored_ports:
            QMessageBox.warning(self, '添加失败', f'端口 {port} 已在监控列表中')
            return
            
        # Common port descriptions
        port_descriptions = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            27017: 'MongoDB'
        }
        
        # Ask for description if it's not a common port
        description = port_descriptions.get(port, '')
        if not description:
            description, ok = QInputDialog.getText(
                self, '端口描述',
                f'请输入端口 {port} 的描述（可选）:',
                text='自定义服务'
            )
            if not ok:
                description = '自定义服务'
        
        try:
            # Add port with description
            self.monitor.monitored_ports.add(port)
            
            # Update port list display
            if not hasattr(self, 'port_list'):
                # Create port list if it doesn't exist
                self.port_list = QTableWidget()
                self.port_list.setColumnCount(4)
                self.port_list.setHorizontalHeaderLabels(['端口', '描述', '状态', '操作'])
                self.port_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
                
                # Find the port layout and add the table
                port_layout = None
                for i in range(self.centralWidget().layout().count()):
                    widget = self.centralWidget().layout().itemAt(i).widget()
                    if isinstance(widget, QTabWidget):
                        ip_tab = widget.widget(0)  # IP Monitor tab
                        for child in ip_tab.children():
                            if isinstance(child, QHBoxLayout) and \
                               any(isinstance(w, QSpinBox) for w in child.children()):
                                port_layout = child.parent()
                                break
                
                if port_layout:
                    port_layout.layout().addWidget(self.port_list)
            
            # Add new port to the list
            row = self.port_list.rowCount()
            self.port_list.insertRow(row)
            self.port_list.setItem(row, 0, QTableWidgetItem(str(port)))
            self.port_list.setItem(row, 1, QTableWidgetItem(description))
            self.port_list.setItem(row, 2, QTableWidgetItem('检查中...'))
            
            # Add remove button
            remove_btn = QPushButton('删除')
            remove_btn.clicked.connect(lambda p=port: self.remove_port_monitor(p))
            self.port_list.setCellWidget(row, 3, remove_btn)
            
            # Refresh status to check the new port
            self.refresh_status()
            
            print(f"添加端口监控: {port} ({description})")
            
        except Exception as e:
            QMessageBox.warning(self, '添加失败', f'添加端口监控时出错: {str(e)}')
    
    def remove_port_monitor(self, port: int):
        """Remove port from monitoring list"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            self.log_message('移除端口监控失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '您没有移除端口监控的权限')
            return
            
        try:
            self.monitor.monitored_ports.remove(port)
            
            # Remove from display
            for row in range(self.port_list.rowCount()):
                if int(self.port_list.item(row, 0).text()) == port:
                    self.port_list.removeRow(row)
                    break
            
            print(f"移除端口监控: {port}")
            self.refresh_status()
            
        except Exception as e:
            QMessageBox.warning(self, '删除失败', f'移除端口监控时出错: {str(e)}')

    def check_network_storm(self):
        """Check for network storm conditions and update display with detailed information"""
        # Check cooldown period for storm alerts
        current_time = time.time()
        if hasattr(self, '_last_storm_alert'):
            if current_time - self._last_storm_alert < self._notification_cooldown:
                return
            
        storm_info = self.monitor.detect_network_storm()
        
        # Create storm status display if not exists
        if not hasattr(self, 'storm_details'):
            self.storm_details = QTextEdit()
            self.storm_details.setReadOnly(True)
            self.storm_details.setMaximumHeight(150)
            
            # Find stats tab and add storm details
            for i in range(self.centralWidget().layout().count()):
                widget = self.centralWidget().layout().itemAt(i).widget()
                if isinstance(widget, QTabWidget):
                    stats_tab = widget.widget(1)  # Network Statistics tab
                    if stats_tab:
                        stats_tab.layout().addWidget(self.storm_details)
        
        # Update storm status information
        if 'error' in storm_info:
            error_type = storm_info.get('error')
            if error_type == 'insufficient_permissions':
                status_text = '网络风暴监测: 需要管理员权限'
                details = (
                    '无法进行网络风暴监测，原因如下：\n'
                    '1. 程序没有足够的系统权限\n'
                    '2. 需要以管理员身份运行\n'
                    '建议：请使用管理员权限重新启动程序'
                )
                style = 'color: orange;'
            elif error_type == 'permission_denied':
                status_text = '网络风暴监测: 无法访问网络接口'
                details = (
                    '无法访问网络接口，可能的原因：\n'
                    '1. 网络接口访问受限\n'
                    '2. 系统防火墙设置\n'
                    '3. 网络驱动程序问题\n'
                    '建议：检查系统设置和网络配置'
                )
                style = 'color: orange;'
            else:
                status_text = f'网络风暴监测: {storm_info["message"]}'
                details = f'发生错误：{storm_info.get("message", "未知错误")}\n建议联系系统管理员'
                style = 'color: orange;'
        else:
            packets = storm_info.get("packets_per_second", 0)
            threshold = storm_info.get("threshold", 1000)
            usage_percent = (packets/threshold*100)
            
            if storm_info.get('detected', False):
                severity = '严重' if packets > threshold * 2 else '中等'
                status_text = (
                    f'警告: 检测到{severity}网络风暴! '
                    f'每秒数据包: {packets:.2f}'
                )
                # Play network storm sound
                self.sound_manager.play_sound('network_storm')
                details = (
                    f'网络风暴详细信息:\n'
                    f'严重程度: {severity}\n'
                    f'当前流量: {packets:.2f} 包/秒\n'
                    f'阈值设置: {threshold} 包/秒\n'
                    f'超出阈值: {((packets/threshold)-1)*100:.1f}%\n\n'
                    f'可能原因:\n'
                    f'1. 网络广播风暴\n'
                    f'2. DDoS攻击\n'
                    f'3. 网络环路\n'
                    f'4. 设备故障\n\n'
                    f'建议操作:\n'
                    f'1. 检查网络设备状态\n'
                    f'2. 隔离可疑设备\n'
                    f'3. 分析网络流量模式'
                )
                style = 'color: red; font-weight: bold;' if packets > threshold * 2 else 'color: orange; font-weight: bold;'
            else:
                status = '良好' if packets < threshold * 0.5 else '正常'
                status_text = f'网络风暴状态: {status}'
                details = (
                    f'网络状态详情:\n'
                    f'当前流量: {packets:.2f} 包/秒\n'
                    f'阈值设置: {threshold} 包/秒\n'
                    f'阈值使用率: {usage_percent:.1f}%\n\n'
                    f'网络健康度: {status}\n'
                    f'• 流量水平: {"低" if usage_percent < 30 else "中等" if usage_percent < 70 else "较高"}\n'
                    f'• 网络状态: {"稳定" if packets < threshold * 0.8 else "需要关注"}'
                )
                style = 'color: green;'
        
        # Update displays with animation
        self.storm_status.setText(status_text)
        self.storm_status.setStyleSheet(style)
        self.storm_details.setText(details)
        self.storm_details.setStyleSheet(style)
        
        # Animate changes
        self.animation_manager.fade_in(self.storm_status)
        self.animation_manager.fade_in(self.storm_details)
        
        # Flash warning for storm detection or errors
        if 'error' in storm_info or storm_info.get('detected', False):
            self.animation_manager.flash_status(
                self.storm_status,
                QColor(255, 0, 0) if storm_info.get('detected', False) else QColor(255, 165, 0),
                duration=2000
            )

    def start_monitoring(self):
        """Start monitoring for all IPs"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, '权限不足', '您没有启动监控的权限')
            return
            
        self.monitoring_active = True
        self.monitored_ips = set(self.monitor.get_all_ips().keys())
        self.refresh_timer.start()
        self.storm_detection_timer.start()
        self.update_button_visibility()
        self.log_message("已启动所有IP的监控", "info")
    
    def stop_monitoring(self):
        """Stop monitoring for all IPs"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, '权限不足', '您没有停止监控的权限')
            return
            
        self.monitoring_active = False
        self.monitored_ips.clear()
        self.refresh_timer.stop()
        self.storm_detection_timer.stop()
        self.update_button_visibility()
        self.log_message("已停止所有IP的监控", "info")
    
    def batch_start(self):
        """Start monitoring for selected IPs"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, '权限不足', '您没有批量启动的权限')
            return
            
        selected_items = self.ip_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '选择错误', '请先选择要启动监控的IP')
            return
            
        selected_rows = set(item.row() for item in selected_items)
        for row in selected_rows:
            ip = self.ip_table.item(row, 0).text()
            self.monitored_ips.add(ip)
        
        if self.monitored_ips:
            self.monitoring_active = True
            self.refresh_timer.start()
            self.storm_detection_timer.start()
            self.update_button_visibility()
            self.log_message(f"已启动 {len(selected_rows)} 个IP的监控", "info")
    
    def batch_stop(self):
        """Stop monitoring for selected IPs"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, '权限不足', '您没有批量停止的权限')
            return
            
        selected_items = self.ip_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '选择错误', '请先选择要停止监控的IP')
            return
            
        selected_rows = set(item.row() for item in selected_items)
        for row in selected_rows:
            ip = self.ip_table.item(row, 0).text()
            self.monitored_ips.discard(ip)
        
        if not self.monitored_ips:
            self.monitoring_active = False
            self.refresh_timer.stop()
            self.storm_detection_timer.stop()
        
        self.update_button_visibility()
        self.log_message(f"已停止 {len(selected_rows)} 个IP的监控", "info")
    
    def start_selected(self):
        """Start monitoring for a single selected IP"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, '权限不足', '您没有启动监控的权限')
            return
            
        selected_items = self.ip_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '选择错误', '请先选择要启动监控的IP')
            return
            
        # Clear existing monitored IPs
        self.monitored_ips.clear()
        
        # Add only the selected IP
        selected_row = selected_items[0].row()
        ip = self.ip_table.item(selected_row, 0).text()
        self.monitored_ips.add(ip)
        
        self.monitoring_active = True
        self.refresh_timer.start()
        self.storm_detection_timer.start()
        self.update_button_visibility()
        self.log_message(f"已启动IP {ip} 的监控", "info")

    def check_session(self):
        """Check if the current session is still valid"""
        if self.session_token and not self.security_manager.validate_session(self.session_token):
            QMessageBox.warning(self, '会话过期', '您的登录会话已过期，请重新登录')
            self.logout()
    
    def update_network_stats(self):
        """Update network statistics display"""
        usage = self.monitor.get_network_usage()
        
        def format_bytes(bytes_val):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if bytes_val < 1024:
                    return f"{bytes_val:.2f} {unit}"
                bytes_val /= 1024
            return f"{bytes_val:.2f} TB"
        
        # Calculate rates (per second)
        if hasattr(self, '_last_stats'):
            time_diff = time.time() - self._last_stats_time
            bytes_sent_rate = (usage['bytes_sent'] - self._last_stats['bytes_sent']) / time_diff
            bytes_recv_rate = (usage['bytes_recv'] - self._last_stats['bytes_recv']) / time_diff
            packets_sent_rate = (usage['packets_sent'] - self._last_stats['packets_sent']) / time_diff
            packets_recv_rate = (usage['packets_recv'] - self._last_stats['packets_recv']) / time_diff
            
            stats_text = "实时网络状态:\n"
            stats_text += f"发送速率: {format_bytes(bytes_sent_rate)}/s\n"
            stats_text += f"接收速率: {format_bytes(bytes_recv_rate)}/s\n"
            stats_text += f"发送包速率: {packets_sent_rate:.2f} 包/秒\n"
            stats_text += f"接收包速率: {packets_recv_rate:.2f} 包/秒\n\n"
            
            # Add network load indicators
            send_load = bytes_sent_rate / (1024*1024*10)  # Assuming 10MB/s as baseline
            recv_load = bytes_recv_rate / (1024*1024*10)
            stats_text += "网络负载:\n"
            stats_text += f"上传负载: {send_load:.1%}\n"
            stats_text += f"下载负载: {recv_load:.1%}\n\n"
        else:
            stats_text = "正在收集网络统计数据...\n\n"
        
        # Add total statistics
        stats_text += "总计统计:\n"
        stats_text += f"发送总量: {format_bytes(usage['bytes_sent'])}\n"
        stats_text += f"接收总量: {format_bytes(usage['bytes_recv'])}\n"
        stats_text += f"发送数据包: {usage['packets_sent']:,}\n"
        stats_text += f"接收数据包: {usage['packets_recv']:,}\n"
        
        # Store current stats for next update
        self._last_stats = usage.copy()
        self._last_stats_time = time.time()
        
        self.stats_text.setText(stats_text)

    def filter_logs(self):
        """Filter log messages based on level and search text"""
        level_filter = self.log_level_combo.currentText()
        search_text = self.log_search.text().lower()
        
        # Get all log entries
        doc = self.log_text.document()
        cursor = QTextCursor(doc)
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        
        # Show/hide based on filters
        while not cursor.atEnd():
            block = cursor.block()
            block_text = block.text().lower()
            
            # Check if matches filters
            level_match = level_filter == '全部' or f'[{level_filter}]' in block_text
            search_match = not search_text or search_text in block_text
            
            # Set block visibility
            block.setVisible(level_match and search_match)
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
    
    def clear_logs(self):
        """Clear all log messages"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            self.log_message('清除日志失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '您没有清除日志的权限')
            return
            
        reply = QMessageBox.question(
            self, '确认清除',
            '确定要清除所有日志记录吗？\n此操作无法撤销。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.log_text.clear()
            self.log_message("日志已清除", "info")
    
    def log_message(self, message: str, level: str = 'info'):
        """Add a message to the log display with timestamp and level, with rate limiting"""
        # Rate limit similar messages
        msg_key = f"{level}:{message}"
        current_time = time.time()
        
        if msg_key in self._message_history:
            last_time = self._message_history[msg_key]
            if current_time - last_time < self._notification_cooldown:
                return  # Skip if message was shown recently
                
        self._message_history[msg_key] = current_time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        level_colors = {
            'info': '#28a745',     # Green
            'warning': '#ffc107',  # Yellow
            'error': '#dc3545',    # Red
            'success': '#17a2b8'   # Blue
        }
        level_icons = {
            'info': '🔵',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        color = level_colors.get(level, '#6c757d')  # Default gray
        icon = level_icons.get(level, 'ℹ️')
        
        # Format log entry with HTML
        log_entry = (
            f'<div style="margin: 2px 0; padding: 2px; border-bottom: 1px solid #eee;">'
            f'<span style="color: #666;">[{timestamp}]</span> '
            f'<span style="color: {color};">{icon} [{level.upper()}]</span> '
            f'{message}'
            f'</div>'
        )
        
        # Add to log display
        self.log_text.append(log_entry)
        
        # Keep only last 1000 messages
        doc = self.log_text.document()
        while doc.blockCount() > 1000:
            cursor = QTextCursor(doc.firstBlock())
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()
        
        # Scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        
        # Also print to console for debugging
        print(f"[{level.upper()}] {message}")

    def refresh_backup_list(self):
        """Refresh the list of available backups"""
        self.backup_list.setRowCount(0)
        backups = self.monitor.backup_manager.list_backups()
        
        for row, backup in enumerate(backups):
            self.backup_list.insertRow(row)
            
            # Parse timestamp from filename
            timestamp = backup.replace("backup_", "").replace(".json", "")
            date_str = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
            
            self.backup_list.setItem(row, 0, QTableWidgetItem(date_str))
            self.backup_list.setItem(row, 1, QTableWidgetItem(backup))
            
            restore_btn = QPushButton('恢复此备份')
            restore_btn.clicked.connect(lambda b=backup: self.restore_backup(b))
            self.backup_list.setCellWidget(row, 2, restore_btn)
            
            # Animate new entries
            for col in range(3):
                widget = self.backup_list.cellWidget(row, col) or self.backup_list.item(row, col)
                if widget:
                    self.animation_manager.fade_in(widget)
    
    def restore_backup(self, backup_file: Optional[str] = None):
        """Restore data from a backup file"""
        if not self.security_manager.has_permission(self.session_token, 'all'):
            self.log_message('恢复备份失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '只有管理员可以恢复备份')
            return
            
        if backup_file is None:
            backups = self.monitor.backup_manager.list_backups()
            if not backups:
                QMessageBox.warning(self, '恢复失败', '没有可用的备份文件')
                return
            backup_file = backups[0]
        
        reply = QMessageBox.question(
            self, '确认恢复',
            f'确定要恢复备份 {backup_file} 吗？\n这将覆盖当前的数据。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.monitor.load_data(os.path.join(self.monitor.backup_manager.backup_dir, backup_file))
            self.refresh_table()
            self.log_message(f"已恢复备份: {backup_file}", "info")
            
            # Animate the refresh
            for row in range(self.ip_table.rowCount()):
                for col in range(self.ip_table.columnCount()):
                    widget = self.ip_table.cellWidget(row, col) or self.ip_table.item(row, col)
                    if widget:
                        self.animation_manager.fade_in(widget)
    
    async def start_discovery(self):
        """Start automatic IP discovery"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, "权限错误", "您没有权限启动IP自动发现")
            return
            
        try:
            # Get current settings
            start_ip = self.start_ip_edit.text().strip()
            end_ip = self.end_ip_edit.text().strip()
            interval = self.interval_edit.value() * 60  # Convert minutes to seconds
            
            # Start discovery in monitor
            self.monitor.set_discovery_range(start_ip, end_ip)
            self.monitor.set_discovery_interval(interval)
            await self.monitor.start_discovery()
            
            # Update UI
            self.start_discovery_button.setEnabled(False)
            self.stop_discovery_button.setEnabled(True)
            self.log_message(f"启动IP自动发现 (范围: {start_ip} - {end_ip}, 间隔: {interval//60}分钟)", "info")
            
        except Exception as e:
            QMessageBox.warning(self, "启动失败", f"启动IP自动发现失败: {str(e)}")
            self.log_message(f"启动IP自动发现失败: {str(e)}", "error")
    
    def stop_discovery(self):
        """Stop automatic IP discovery"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, "权限错误", "您没有权限停止IP自动发现")
            return
            
        try:
            self.monitor.stop_discovery()
            self.start_discovery_button.setEnabled(True)
            self.stop_discovery_button.setEnabled(False)
            self.log_message("停止IP自动发现", "info")
        except Exception as e:
            QMessageBox.warning(self, "停止失败", f"停止IP自动发现失败: {str(e)}")
            self.log_message(f"停止IP自动发现失败: {str(e)}", "error")
    
    def set_discovery_range(self):
        """Set IP range for discovery"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, "权限错误", "您没有权限配置IP自动发现")
            return
            
        try:
            start_ip = self.start_ip_edit.text().strip()
            end_ip = self.end_ip_edit.text().strip()
            self.monitor.set_discovery_range(start_ip, end_ip)
            self.log_message(f"设置IP扫描范围: {start_ip} - {end_ip}", "info")
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            self.log_message(f"设置IP扫描范围失败: {str(e)}", "error")
    
    def set_discovery_interval(self):
        """Set interval for discovery"""
        if not self.security_manager.has_permission(self.session_token, 'edit_ip'):
            QMessageBox.warning(self, "权限错误", "您没有权限配置IP自动发现")
            return
            
        try:
            interval = self.interval_edit.value() * 60  # Convert minutes to seconds
            self.monitor.set_discovery_interval(interval)
            self.log_message(f"设置IP扫描间隔: {interval//60}分钟", "info")
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            self.log_message(f"设置IP扫描间隔失败: {str(e)}", "error")
    
    def export_data(self):
        """Export comprehensive monitoring data to file with format selection"""
        if not self.security_manager.has_permission(self.session_token, 'export_data'):
            self.log_message('导出数据失败：权限不足', 'error')
            QMessageBox.warning(self, '权限不足', '您没有导出数据的权限')
            return
            
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_name = f"network_monitor_export_{timestamp}"
            
            filepath, selected_filter = QFileDialog.getSaveFileName(
                self,
                "导出数据",
                default_name,
                "CSV Files (*.csv);;Excel Files (*.xlsx);;JSON Files (*.json)"
            )
            
            if not filepath:
                return
                
            # Determine export format from selected filter
            if selected_filter == "CSV Files (*.csv)":
                self._export_csv(filepath)
            elif selected_filter == "Excel Files (*.xlsx)":
                self._export_excel(filepath)
            elif selected_filter == "JSON Files (*.json)":
                self._export_json(filepath)
                
            QMessageBox.information(self, "导出成功", f"数据已导出至: {filepath}")
            
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出数据时出错: {str(e)}")
    
    def _export_csv(self, filepath):
        """Export data to CSV format"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['IP地址', '描述', '状态', '端口状态', '最后更新', '历史记录'])
            
            for row in range(self.ip_table.rowCount()):
                ip = self.ip_table.item(row, 0).text()
                desc = self.ip_table.item(row, 1).text()
                status = self.ip_table.item(row, 2).text()
                ports = self.ip_table.item(row, 3).text()
                history = self.monitor.get_ip_history(ip) if hasattr(self.monitor, 'get_ip_history') else ''
                
                writer.writerow([
                    ip, desc, status, ports,
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    history
                ])
    
    def _export_excel(self, filepath):
        """Export data to Excel format"""
        try:
            import pandas as pd
            
            data = []
            for row in range(self.ip_table.rowCount()):
                ip = self.ip_table.item(row, 0).text()
                desc = self.ip_table.item(row, 1).text()
                status = self.ip_table.item(row, 2).text()
                ports = self.ip_table.item(row, 3).text()
                history = self.monitor.get_ip_history(ip) if hasattr(self.monitor, 'get_ip_history') else ''
                
                data.append({
                    'IP地址': ip,
                    '描述': desc,
                    '状态': status,
                    '端口状态': ports,
                    '最后更新': time.strftime("%Y-%m-%d %H:%M:%S"),
                    '历史记录': history
                })
                
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, engine='openpyxl')
            
        except ImportError:
            raise Exception("导出Excel需要安装pandas和openpyxl库")
    
    def _export_json(self, filepath):
        """Export data to JSON format"""
        network_usage = self.monitor.get_network_usage()
        storm_info = self.monitor.detect_network_storm()
        
        # Calculate rates if available
        network_rates = {}
        if hasattr(self, '_last_stats'):
            time_diff = time.time() - self._last_stats_time
            network_rates = {
                'bytes_sent_rate': self.format_bytes((network_usage['bytes_sent'] - self._last_stats['bytes_sent']) / time_diff) + '/s',
                'bytes_recv_rate': self.format_bytes((network_usage['bytes_recv'] - self._last_stats['bytes_recv']) / time_diff) + '/s',
                'packets_sent_rate': f"{(network_usage['packets_sent'] - self._last_stats['packets_sent']) / time_diff:.2f} 包/秒",
                'packets_recv_rate': f"{(network_usage['packets_recv'] - self._last_stats['packets_recv']) / time_diff:.2f} 包/秒"
            }
        
        data = {
            'export_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'monitored_ips': {},
            'monitored_ports': list(self.monitor.monitored_ports),
            'network_statistics': {
                'bytes_sent': self.format_bytes(network_usage['bytes_sent']),
                'bytes_recv': self.format_bytes(network_usage['bytes_recv']),
                'packets_sent': network_usage['packets_sent'],
                'packets_recv': network_usage['packets_recv'],
                'current_rates': network_rates
            },
            'storm_detection': {
                'status': '正常' if not storm_info.get('detected', False) else '检测到风暴',
                'packets_per_second': storm_info.get('packets_per_second', 0),
                'threshold': storm_info.get('threshold', 1000),
                'error': storm_info.get('error', None)
            },
            'system_info': {
                'interfaces': self.monitor.get_network_interfaces(),
                'monitoring_start_time': getattr(self.monitor, 'start_time', time.strftime("%Y-%m-%d %H:%M:%S")),
                'export_version': '1.0'
            }
        }
        
        # Add IP data with history
        for row in range(self.ip_table.rowCount()):
            ip = self.ip_table.item(row, 0).text()
            desc = self.ip_table.item(row, 1).text()
            status = self.ip_table.item(row, 2).text()
            ports = self.ip_table.item(row, 3).text()
            history = self.monitor.get_ip_history(ip) if hasattr(self.monitor, 'get_ip_history') else ''
            
            data['monitored_ips'][ip] = {
                'description': desc,
                'status': status,
                'ports': ports,
                'history': history
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def import_data(self):
        """Import IP data from file"""
        try:
            filepath, selected_filter = QFileDialog.getOpenFileName(
                self,
                "导入数据",
                "",
                "CSV Files (*.csv);;Excel Files (*.xlsx);;JSON Files (*.json)"
            )
            
            if not filepath:
                return
                
            # Determine import format from selected filter
            if selected_filter == "CSV Files (*.csv)":
                self._import_csv(filepath)
            elif selected_filter == "Excel Files (*.xlsx)":
                self._import_excel(filepath)
            elif selected_filter == "JSON Files (*.json)":
                self._import_json(filepath)
                
            self.refresh_table()
            QMessageBox.information(self, "导入成功", "数据导入完成")
            
        except Exception as e:
            QMessageBox.warning(self, "导入失败", f"导入数据时出错: {str(e)}")
    
    def _import_csv(self, filepath):
        """Import data from CSV file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip = row.get('IP地址')
                desc = row.get('描述')
                if ip and desc:
                    self.monitor.add_ip(ip, desc)
    
    def _import_excel(self, filepath):
        """Import data from Excel file"""
        try:
            import pandas as pd
            df = pd.read_excel(filepath, engine='openpyxl')
            for _, row in df.iterrows():
                ip = row.get('IP地址')
                desc = row.get('描述')
                if ip and desc:
                    self.monitor.add_ip(ip, desc)
        except ImportError:
            raise Exception("导入Excel需要安装pandas和openpyxl库")
    
    def _import_json(self, filepath):
        """Import data from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'monitored_ips' in data:
                # New format
                for ip, info in data['monitored_ips'].items():
                    desc = info.get('description')
                    if ip and desc:
                        self.monitor.add_ip(ip, desc)
            else:
                # Old format or simple list
                for item in data:
                    ip = item.get('ip')
                    desc = item.get('description')
                    if ip and desc:
                        self.monitor.add_ip(ip, desc)
    
    def batch_modify_descriptions(self):
        """Batch modify IP descriptions"""
        try:
            filepath, selected_filter = QFileDialog.getOpenFileName(
                self,
                "选择描述文件",
                "",
                "CSV Files (*.csv);;Excel Files (*.xlsx);;JSON Files (*.json)"
            )
            
            if not filepath:
                return
                
            updates = {}
            
            # Parse file based on format
            if selected_filter == "CSV Files (*.csv)":
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        ip = row.get('IP地址')
                        desc = row.get('描述')
                        if ip and desc:
                            updates[ip] = desc
                            
            elif selected_filter == "Excel Files (*.xlsx)":
                import pandas as pd
                df = pd.read_excel(filepath, engine='openpyxl')
                for _, row in df.iterrows():
                    ip = row.get('IP地址')
                    desc = row.get('描述')
                    if ip and desc:
                        updates[ip] = desc
                        
            elif selected_filter == "JSON Files (*.json)":
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'monitored_ips' in data:
                        # New format
                        for ip, info in data['monitored_ips'].items():
                            desc = info.get('description')
                            if ip and desc:
                                updates[ip] = desc
                    else:
                        # Old format or simple list
                        for item in data:
                            ip = item.get('ip')
                            desc = item.get('description')
                            if ip and desc:
                                updates[ip] = desc
            
            # Update descriptions
            for ip, desc in updates.items():
                self.monitor.update_description(ip, desc)
            
            self.refresh_table()
            QMessageBox.information(
                self,
                "批量修改完成",
                f"已更新 {len(updates)} 个IP描述"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "批量修改失败",
                f"修改IP描述时出错: {str(e)}"
            )
