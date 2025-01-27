import sys
import os
import signal
import time
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from network_monitor.ui.main_window import MainWindow
from network_monitor.core.security_manager import SecurityManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\n收到中断信号，正在关闭应用...")
    QApplication.quit()

def main():
    try:
        # Use offscreen platform for headless environment
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        logging.info("正在使用 offscreen 平台插件初始化...")
        
        # Set up signal handling
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Initialize security manager
        logging.info("初始化安全管理器...")
        security_manager = SecurityManager()
        
        logging.info("创建 QApplication...")
        app = QApplication(sys.argv)
        
        logging.info("创建主窗口...")
        window = MainWindow(security_manager)
        
        logging.info("显示主窗口...")
        window.show()
        
        # For testing purposes, create a timer to quit after 2 minutes
        if "--test" in sys.argv:
            logging.info("测试模式：应用将在2分钟后自动关闭")
            quit_timer = QTimer()
            quit_timer.timeout.connect(app.quit)
            quit_timer.start(120000)  # 2 minutes
            
    except Exception as e:
        logging.error(f"初始化失败: {str(e)}")
        if "minimal" in str(e):
            logging.info("尝试使用 offscreen 平台插件...")
            os.environ["QT_QPA_PLATFORM"] = "offscreen"
            return main()  # Retry with offscreen platform
        return 1
    
    try:
        return app.exec()
    except KeyboardInterrupt:
        print("\n应用正在关闭...")
        return 0
    finally:
        print("清理资源...")
        # Add any cleanup code here if needed

if __name__ == '__main__':
    sys.exit(main())
