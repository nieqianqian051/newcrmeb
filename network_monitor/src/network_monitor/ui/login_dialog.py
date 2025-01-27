from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    """Dialog for user authentication"""
    
    def __init__(self, security_manager, parent=None):
        super().__init__(parent)
        self.security_manager = security_manager
        self.session_token = None
        
        self.setWindowTitle("登录")
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:")
        self.username_edit = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        layout.addLayout(username_layout)
        
        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        layout.addLayout(password_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("登录")
        login_button.clicked.connect(self.try_login)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(login_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set focus to username field
        self.username_edit.setFocus()
        
        # Connect enter key to login
        self.username_edit.returnPressed.connect(self.try_login)
        self.password_edit.returnPressed.connect(self.try_login)
    
    def try_login(self):
        """Attempt to log in with provided credentials"""
        username = self.username_edit.text()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return
        
        token = self.security_manager.authenticate(username, password)
        if token:
            self.session_token = token
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误")
            self.password_edit.clear()
            self.password_edit.setFocus()
    
    def get_session_token(self):
        """Return the session token if login was successful"""
        return self.session_token
