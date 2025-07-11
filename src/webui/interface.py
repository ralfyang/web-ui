import gradio as gr
from src.webui.webui_manager import WebuiManager
from src.webui.session_auth import AuthManager
from src.webui.components.auth_components import (
    create_login_form, 
    create_logout_button, 
    setup_login_events, 
    setup_logout_events
)
from src.webui.components.main_app_components import create_main_application
from src.webui.auth_handlers import (
    initialize_auth_manager, 
    handle_login, 
    handle_logout
)
from src.webui.styles import get_combined_styles

# 테마 맵
theme_map = {
    "Default": gr.themes.Default(),
    "Soft": gr.themes.Soft(),
    "Monochrome": gr.themes.Monochrome(),
    "Glass": gr.themes.Glass(),
    "Origin": gr.themes.Origin(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Base": gr.themes.Base()
}


def create_ui(theme_name="Ocean", enable_auth=True):
    """UI 생성 - 인증 여부에 따라 다른 인터페이스 반환"""
    
    if not enable_auth:
        # 인증 비활성화 시 기존 인터페이스 반환
        return create_main_interface_without_auth(theme_name), False
    
    # 인증 활성화 시 로그인 시스템 사용
    auth_manager = initialize_auth_manager()
    
    js_func = """
    function refresh() {
        const url = new URL(window.location);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.href = url.href;
        }
    }
    """

    with gr.Blocks(
        title="Browser Use WebUI", 
        theme=theme_map[theme_name], 
        css=get_combined_styles(), 
        js=js_func
    ) as demo:
        
        # 로그인 폼 생성
        login_form, login_components = create_login_form()
        
        # 메인 애플리케이션 (로그인 후 표시)
        with gr.Group(visible=False) as main_app:
            ui_manager = WebuiManager()
            logout_button = create_logout_button()
            create_main_application(ui_manager, logout_button)
            
            # 로그아웃 이벤트 설정
            setup_logout_events(
                logout_button, 
                login_form, 
                main_app, 
                login_components, 
                handle_logout
            )
        
        # 로그인 이벤트 설정
        setup_login_events(
            login_components, 
            login_form, 
            main_app, 
            handle_login
        )
    
    return demo, enable_auth


def create_main_interface_without_auth(theme_name="Ocean"):
    """인증 없는 메인 인터페이스 (기존 방식)"""
    js_func = """
    function refresh() {
        const url = new URL(window.location);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.href = url.href;
        }
    }
    """

    ui_manager = WebuiManager()

    with gr.Blocks(
        title="Browser Use WebUI", 
        theme=theme_map[theme_name], 
        css=get_combined_styles(), 
        js=js_func
    ) as demo:
        # 더미 로그아웃 버튼 (표시되지 않음)
        logout_button = gr.Button(visible=False)
        create_main_application(ui_manager, logout_button)
    
    return demo