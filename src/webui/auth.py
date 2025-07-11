import os
import hashlib
import secrets
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class AuthManager:
    """인증 관리 클래스"""
    
    def __init__(self):
        self.users = self._load_users()
        
    def _load_users(self) -> dict:
        """환경변수 또는 기본값에서 사용자 정보 로드"""
        users = {}
        
        # 환경변수에서 사용자 정보 로드
        auth_users = os.getenv("AUTH_USERS", "")
        if auth_users:
            # 형식: "user1:password1,user2:password2"
            for user_info in auth_users.split(","):
                if ":" in user_info:
                    username, password = user_info.strip().split(":", 1)
                    users[username] = self._hash_password(password)
        
        # 기본 관리자 계정 (환경변수가 없는 경우)
        if not users:
            default_username = os.getenv("DEFAULT_USERNAME", "admin")
            default_password = os.getenv("DEFAULT_PASSWORD", "browser-use-2024")
            users[default_username] = self._hash_password(default_password)
            logger.info(f"기본 관리자 계정 생성: {default_username}")
        
        return users
    
    def _hash_password(self, password: str) -> str:
        """비밀번호 해시화"""
        salt = os.getenv("PASSWORD_SALT", "browser-use-salt")
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        """사용자 인증"""
        if username not in self.users:
            return False
        
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password
    
    def get_auth_function(self):
        """Gradio 인증 함수 반환"""
        def auth_func(username: str, password: str) -> bool:
            return self.authenticate(username, password)
        return auth_func


def create_auth_manager() -> AuthManager:
    """인증 매니저 생성"""
    return AuthManager()