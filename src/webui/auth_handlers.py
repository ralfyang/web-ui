import logging
from typing import Tuple, Dict, Any
import gradio as gr
from src.webui.session_auth import AuthManager

logger = logging.getLogger(__name__)

# 전역 변수
global_auth_manager = None
current_session_id = None


def initialize_auth_manager() -> AuthManager:
    """인증 매니저 초기화"""
    global global_auth_manager
    if global_auth_manager is None:
        global_auth_manager = AuthManager()
    return global_auth_manager


def handle_login(username: str, password: str) -> Tuple[gr.update, gr.update, str]:
    """로그인 처리"""
    global current_session_id, global_auth_manager
    
    if not username or not password:
        return (
            gr.update(visible=True),   # login_form
            gr.update(visible=False),  # main_app  
            "사용자명과 비밀번호를 입력하세요."  # error_message
        )
    
    if global_auth_manager is None:
        global_auth_manager = initialize_auth_manager()
    
    session_id = global_auth_manager.authenticate(username, password)
    if session_id:
        current_session_id = session_id
        logger.info(f"사용자 로그인 성공: {username}")
        return (
            gr.update(visible=False),  # login_form
            gr.update(visible=True),   # main_app
            ""  # error_message
        )
    else:
        logger.warning(f"로그인 실패: {username}")
        return (
            gr.update(visible=True),   # login_form
            gr.update(visible=False),  # main_app
            "잘못된 사용자명 또는 비밀번호입니다."  # error_message
        )


def handle_logout() -> Tuple[gr.update, gr.update, str, str, str]:
    """로그아웃 처리"""
    global current_session_id, global_auth_manager
    
    if current_session_id and global_auth_manager:
        username = global_auth_manager.validate_session(current_session_id)
        global_auth_manager.logout(current_session_id)
        current_session_id = None
        logger.info(f"사용자 로그아웃: {username}")
    
    return (
        gr.update(visible=True),   # login_form 표시
        gr.update(visible=False),  # main_app 숨김
        "",                        # error_message 초기화
        "",                        # username 초기화
        ""                         # password 초기화
    )


def get_current_session_info() -> Dict[str, Any]:
    """현재 세션 정보 반환"""
    global current_session_id, global_auth_manager
    
    if current_session_id and global_auth_manager:
        username = global_auth_manager.validate_session(current_session_id)
        return {
            "session_id": current_session_id,
            "username": username,
            "authenticated": username is not None
        }
    
    return {
        "session_id": None,
        "username": None,
        "authenticated": False
    }