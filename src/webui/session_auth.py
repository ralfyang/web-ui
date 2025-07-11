import os
import hashlib
import secrets
import time
from typing import Optional, Dict, Set
import logging
import gradio as gr

logger = logging.getLogger(__name__)


class SessionManager:
    """세션 관리 클래스"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}  # session_id -> session_data
        self.session_timeout = 3600 * 8  # 8시간
        
    def create_session(self, username: str) -> str:
        """새 세션 생성"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'username': username,
            'created_at': time.time(),
            'last_access': time.time()
        }
        logger.info(f"새 세션 생성: {username} (ID: {session_id[:8]}...)")
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[str]:
        """세션 유효성 검증"""
        if not session_id or session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        current_time = time.time()
        
        # 세션 만료 확인
        if current_time - session['last_access'] > self.session_timeout:
            self.destroy_session(session_id)
            return None
            
        # 마지막 접근 시간 업데이트
        session['last_access'] = current_time
        return session['username']
    
    def destroy_session(self, session_id: str) -> bool:
        """세션 삭제"""
        if session_id in self.sessions:
            username = self.sessions[session_id]['username']
            del self.sessions[session_id]
            logger.info(f"세션 삭제: {username} (ID: {session_id[:8]}...)")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """만료된 세션 정리"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session['last_access'] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)


class AuthManager:
    """인증 관리 클래스"""
    
    def __init__(self):
        self.users = self._load_users()
        self.session_manager = SessionManager()
        
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
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """사용자 인증 및 세션 생성"""
        if username not in self.users:
            logger.warning(f"존재하지 않는 사용자: {username}")
            return None
        
        hashed_password = self._hash_password(password)
        if self.users[username] == hashed_password:
            session_id = self.session_manager.create_session(username)
            logger.info(f"로그인 성공: {username}")
            return session_id
        else:
            logger.warning(f"로그인 실패: {username}")
            return None
    
    def validate_session(self, session_id: str) -> Optional[str]:
        """세션 유효성 검증"""
        return self.session_manager.validate_session(session_id)
    
    def logout(self, session_id: str) -> bool:
        """로그아웃"""
        return self.session_manager.destroy_session(session_id)


def create_login_interface(auth_manager: AuthManager):
    """로그인 인터페이스 생성"""
    
    def handle_login(username: str, password: str, request: gr.Request):
        """로그인 처리"""
        if not username or not password:
            return gr.update(visible=True), gr.update(visible=False), "사용자명과 비밀번호를 입력하세요."
        
        session_id = auth_manager.authenticate(username, password)
        if session_id:
            # 세션 ID를 쿠키에 저장
            response = gr.update(visible=False), gr.update(visible=True), ""
            # Gradio에서 쿠키 설정은 제한적이므로 세션 상태를 다른 방식으로 관리
            return response
        else:
            return gr.update(visible=True), gr.update(visible=False), "잘못된 사용자명 또는 비밀번호입니다."
    
    def handle_logout(request: gr.Request):
        """로그아웃 처리"""
        # 세션 정리 로직
        return gr.update(visible=True), gr.update(visible=False), ""
    
    with gr.Blocks(title="Browser Use WebUI - 로그인") as login_interface:
        with gr.Column(elem_classes=["login-container"]):
            gr.Markdown("# 🔐 Browser Use WebUI 로그인")
            
            with gr.Group():
                username_input = gr.Textbox(
                    label="사용자명",
                    placeholder="사용자명을 입력하세요",
                    elem_id="username"
                )
                password_input = gr.Textbox(
                    label="비밀번호",
                    type="password",
                    placeholder="비밀번호를 입력하세요",
                    elem_id="password"
                )
                login_button = gr.Button("로그인", variant="primary", elem_id="login-btn")
                error_message = gr.Markdown("", elem_classes=["error-message"])
        
        # 상태 관리
        login_form = gr.Group(visible=True)
        main_app = gr.Group(visible=False)
        
        login_button.click(
            fn=handle_login,
            inputs=[username_input, password_input],
            outputs=[login_form, main_app, error_message]
        )
        
        password_input.submit(
            fn=handle_login,
            inputs=[username_input, password_input],
            outputs=[login_form, main_app, error_message]
        )
    
    return login_interface


def create_auth_wrapper(auth_manager: AuthManager, main_interface):
    """인증 래퍼 생성"""
    
    def check_auth_and_render(request: gr.Request):
        """인증 확인 및 인터페이스 렌더링"""
        # 여기서 세션 확인 로직 구현
        # 실제 구현에서는 request에서 세션 정보를 추출해야 함
        return main_interface
    
    return check_auth_and_render