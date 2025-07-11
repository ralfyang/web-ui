import gradio as gr
from typing import Callable, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_login_form() -> Tuple[gr.Group, Dict[str, gr.Component]]:
    """로그인 폼 컴포넌트 생성"""
    components = {}
    
    with gr.Group(visible=True) as login_form:
        with gr.Column(elem_classes=["login-container"]):
            gr.Markdown("# 🔐 Browser Use WebUI")
            gr.Markdown("### 로그인이 필요합니다")
            
            components["username_input"] = gr.Textbox(
                label="사용자명",
                placeholder="사용자명을 입력하세요",
                elem_id="username"
            )
            components["password_input"] = gr.Textbox(
                label="비밀번호",
                type="password",
                placeholder="비밀번호를 입력하세요",
                elem_id="password"
            )
            components["login_button"] = gr.Button(
                "로그인", 
                variant="primary", 
                elem_id="login-btn"
            )
            components["error_message"] = gr.Markdown(
                "", 
                elem_classes=["error-message"]
            )
    
    return login_form, components


def create_logout_button() -> gr.Button:
    """로그아웃 버튼 생성"""
    return gr.Button(
        "🚪 로그아웃", 
        elem_classes=["logout-button"],
        size="sm",
        variant="stop"
    )


def setup_login_events(
    login_components: Dict[str, gr.Component],
    login_form: gr.Group,
    main_app: gr.Group,
    handle_login_func: Callable
) -> None:
    """로그인 이벤트 설정"""
    login_components["login_button"].click(
        fn=handle_login_func,
        inputs=[
            login_components["username_input"], 
            login_components["password_input"]
        ],
        outputs=[
            login_form, 
            main_app, 
            login_components["error_message"]
        ]
    )
    
    login_components["password_input"].submit(
        fn=handle_login_func,
        inputs=[
            login_components["username_input"], 
            login_components["password_input"]
        ],
        outputs=[
            login_form, 
            main_app, 
            login_components["error_message"]
        ]
    )


def setup_logout_events(
    logout_button: gr.Button,
    login_form: gr.Group,
    main_app: gr.Group,
    login_components: Dict[str, gr.Component],
    handle_logout_func: Callable
) -> None:
    """로그아웃 이벤트 설정"""
    logout_button.click(
        fn=handle_logout_func,
        inputs=[],
        outputs=[
            login_form, 
            main_app, 
            login_components["error_message"], 
            login_components["username_input"], 
            login_components["password_input"]
        ]
    )