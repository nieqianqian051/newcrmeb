import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class SecurityManager:
    """Manages authentication and authorization for the network monitor application"""
    
    ROLES = {
        'admin': ['all'],  # Admin has all permissions
        'operator': [
            'view_status',
            'add_ip',
            'edit_ip',
            'start_monitoring',
            'stop_monitoring',
            'export_data',
            'import_data'
        ],
        'viewer': [
            'view_status',
            'export_data'
        ]
    }
    
    def __init__(self, config_dir: str = "config"):
        """Initialize the security manager"""
        self.config_dir = os.path.abspath(config_dir)
        self.users_file = os.path.join(self.config_dir, "users.json")
        self.sessions: Dict[str, Dict] = {}  # token -> session data
        self.session_timeout = timedelta(hours=12)
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load or create users file
        self._load_users()
        
        # Create default admin if no users exist
        if not self.users:
            self._create_default_admin()
    
    def _load_users(self):
        """Load users from file or create empty user dict"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
    
    def _save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _create_default_admin(self):
        """Create default admin account if no users exist"""
        self.create_user("admin", "admin123", "admin")
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, role: str) -> bool:
        """Create a new user"""
        if username in self.users:
            return False
            
        if role not in self.ROLES:
            return False
            
        self.users[username] = {
            'password_hash': self._hash_password(password),
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        self._save_users()
        return True
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate a user and return a session token
        
        Returns:
            str: Session token if authentication successful, None otherwise
        """
        user = self.users.get(username)
        if not user:
            return None
            
        if user['password_hash'] != self._hash_password(password):
            return None
            
        # Create session token
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            'username': username,
            'role': user['role'],
            'created_at': datetime.now().isoformat()
        }
        
        return token
    
    def validate_session(self, token: str) -> bool:
        """Check if a session token is valid"""
        session = self.sessions.get(token)
        if not session:
            return False
            
        created_at = datetime.fromisoformat(session['created_at'])
        if datetime.now() - created_at > self.session_timeout:
            del self.sessions[token]
            return False
            
        return True
    
    def get_user_role(self, token: str) -> Optional[str]:
        """Get the role of the user associated with a session token"""
        session = self.sessions.get(token)
        return session['role'] if session else None
    
    def has_permission(self, token: str, permission: str) -> bool:
        """Check if a user has a specific permission"""
        session = self.sessions.get(token)
        if not session:
            return False
            
        role = session['role']
        role_permissions = self.ROLES.get(role, [])
        
        return 'all' in role_permissions or permission in role_permissions
    
    def logout(self, token: str):
        """Invalidate a session token"""
        if token in self.sessions:
            del self.sessions[token]
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change a user's password"""
        user = self.users.get(username)
        if not user:
            return False
            
        if user['password_hash'] != self._hash_password(old_password):
            return False
            
        user['password_hash'] = self._hash_password(new_password)
        self._save_users()
        return True
    
    def get_users(self) -> List[Dict]:
        """Get list of users (without password hashes)"""
        return [
            {
                'username': username,
                'role': data['role'],
                'created_at': data['created_at']
            }
            for username, data in self.users.items()
        ]
