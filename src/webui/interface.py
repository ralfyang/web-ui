import gradio as gr

from src.webui.webui_manager import WebuiManager
from src.webui.session_auth import AuthManager, create_login_interface
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab

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

# 전역 인증 관리자
global_auth_manager = None
current_session_id = None


def create_authenticated_interface(auth_manager: AuthManager):
    """인증된 사용자를 위한 메인 인터페이스"""
    ui_manager = WebuiManager()
    
    def handle_logout():
        """로그아웃 처리"""
        global current_session_id
        if current_session_id:
            auth_manager.logout(current_session_id)
            current_session_id = None
        
        # JavaScript를 통한 페이지 새로고침
        return gr.HTML("""
            <script>
            setTimeout(function() {
                window.location.href = window.location.origin + window.location.pathname;
            }, 500);
            </script>
            <div style="text-align: center; padding: 20px;">
                <h3>로그아웃 중...</h3>
                <p>잠시 후 로그인 화면으로 이동합니다.</p>
            </div>
        """)
    
    css = """
    .gradio-container {
        width: 70vw !important; 
        max-width: 70% !important; 
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 10px !important;
    }
    .header-text {
        text-align: center;
        margin-bottom: 20px;
    }
    .tab-header-text {
        text-align: center;
    }
    .theme-section {
        margin-bottom: 10px;
        padding: 15px;
        border-radius: 10px;
    }
    .logout-button {
        position: fixed !important;
        top: 10px !important;
        right: 10px !important;
        z-index: 1000 !important;
        background: #ff4444 !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        font-size: 12px !important;
    }
    .logout-button:hover {
        background: #cc3333 !important;
    }
    """

    js_func = """
    function refresh() {
        const url = new URL(window.location);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.href = url.href;
        }
    }
    """

    with gr.Blocks(title="Browser Use WebUI", theme=theme_map["Ocean"], css=css, js=js_func) as main_interface:
        # 로그아웃 관련 컴포넌트
        logout_output = gr.HTML(visible=False)
        
        with gr.Row():
            with gr.Column(scale=10):
                gr.Markdown(
                    """
                    # 🌐 Browser Use WebUI
                    ### Control your browser with AI assistance
                    """,
                    elem_classes=["header-text"],
                )
            with gr.Column(scale=1, min_width=100):
                logout_btn = gr.Button(
                    "🚪 로그아웃", 
                    elem_classes=["logout-button"],
                    size="sm",
                    variant="stop"
                )

        with gr.Tabs() as tabs:
            with gr.TabItem("⚙️ Agent Settings"):
                create_agent_settings_tab(ui_manager)

            with gr.TabItem("🌐 Browser Settings"):
                create_browser_settings_tab(ui_manager)

            with gr.TabItem("🤖 Run Agent"):
                create_browser_use_agent_tab(ui_manager)

            with gr.TabItem("🎁 Agent Marketplace"):
                gr.Markdown(
                    """
                    ### Agents built on Browser-Use
                    """,
                    elem_classes=["tab-header-text"],
                )
                with gr.Tabs():
                    with gr.TabItem("Deep Research"):
                        create_deep_research_agent_tab(ui_manager)

            with gr.TabItem("📁 Load & Save Config"):
                create_load_save_config_tab(ui_manager)

        # 로그아웃 버튼 이벤트 연결
        logout_btn.click(
            fn=handle_logout,
            inputs=[],
            outputs=[logout_output]
        )
    
    return main_interface


def create_ui(theme_name="Ocean", enable_auth=True):
    """UI 생성 - 인증 여부에 따라 다른 인터페이스 반환"""
    global global_auth_manager
    
    if not enable_auth:
        # 인증 비활성화 시 기존 인터페이스 반환
        return create_main_interface_without_auth(theme_name), False
    
    # 인증 활성화 시 로그인 시스템 사용
    global_auth_manager = AuthManager()
    
    def handle_login(username: str, password: str):
        """로그인 처리"""
        global current_session_id
        
        if not username or not password:
            return (
                gr.update(visible=True),  # login_form
                gr.update(visible=False), # main_app  
                "사용자명과 비밀번호를 입력하세요."  # error_message
            )
        
        session_id = global_auth_manager.authenticate(username, password)
        if session_id:
            current_session_id = session_id
            return (
                gr.update(visible=False), # login_form
                gr.update(visible=True),  # main_app
                ""  # error_message
            )
        else:
            return (
                gr.update(visible=True),  # login_form
                gr.update(visible=False), # main_app
                "잘못된 사용자명 또는 비밀번호입니다."  # error_message
            )
    
    # 로그인 인터페이스와 메인 인터페이스를 결합
    css = """
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .error-message {
        color: #ff4444;
        text-align: center;
        margin-top: 10px;
    }
    .gradio-container {
        width: 70vw !important; 
        max-width: 70% !important; 
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 10px !important;
    }
    .header-text {
        text-align: center;
        margin-bottom: 20px;
    }
    .tab-header-text {
        text-align: center;
    }
    .theme-section {
        margin-bottom: 10px;
        padding: 15px;
        border-radius: 10px;
    }
    .logout-button {
        position: fixed !important;
        top: 10px !important;
        right: 10px !important;
        z-index: 1000 !important;
        background: #ff4444 !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        font-size: 12px !important;
    }
    .logout-button:hover {
        background: #cc3333 !important;
    }
    """

    js_func = """
    function refresh() {
        const url = new URL(window.location);

        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.href = url.href;
        }
    }
    """

    with gr.Blocks(title="Browser Use WebUI", theme=theme_map[theme_name], css=css, js=js_func) as demo:
        # 로그인 폼
        with gr.Group(visible=True) as login_form:
            with gr.Column(elem_classes=["login-container"]):
                gr.Markdown("# 🔐 Browser Use WebUI")
                gr.Markdown("### 로그인이 필요합니다")
                
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
        
        # 메인 애플리케이션 (로그인 후 표시)
        with gr.Group(visible=False) as main_app:
            main_interface = create_authenticated_interface(global_auth_manager)
            # 메인 인터페이스의 내용을 여기에 복사
            with gr.Row():
                with gr.Column(scale=10):
                    gr.Markdown(
                        """
                        # 🌐 Browser Use WebUI
                        ### Control your browser with AI assistance
                        """,
                        elem_classes=["header-text"],
                    )
                with gr.Column(scale=1, min_width=100):
                    logout_btn = gr.Button(
                        "🚪 로그아웃", 
                        elem_classes=["logout-button"],
                        size="sm",
                        variant="stop"
                    )
            
            ui_manager = WebuiManager()
            with gr.Tabs():
                with gr.TabItem("⚙️ Agent Settings"):
                    create_agent_settings_tab(ui_manager)
                with gr.TabItem("🌐 Browser Settings"):
                    create_browser_settings_tab(ui_manager)
                with gr.TabItem("🤖 Run Agent"):
                    create_browser_use_agent_tab(ui_manager)
                with gr.TabItem("🎁 Agent Marketplace"):
                    gr.Markdown("### Agents built on Browser-Use", elem_classes=["tab-header-text"])
                    with gr.Tabs():
                        with gr.TabItem("Deep Research"):
                            create_deep_research_agent_tab(ui_manager)
                with gr.TabItem("📁 Load & Save Config"):
                    create_load_save_config_tab(ui_manager)
            
            # 로그아웃 처리
            def handle_main_logout():
                global current_session_id
                if current_session_id:
                    global_auth_manager.logout(current_session_id)
                    current_session_id = None
                return (
                    gr.update(visible=True),   # login_form 표시
                    gr.update(visible=False),  # main_app 숨김
                    "",                        # error_message 초기화
                    "",                        # username 초기화
                    ""                         # password 초기화
                )
            
            logout_btn.click(
                fn=handle_main_logout,
                inputs=[],
                outputs=[login_form, main_app, error_message, username_input, password_input]
            )
        
        # 로그인 이벤트 연결
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
    
    return demo, enable_auth


def create_main_interface_without_auth(theme_name="Ocean"):
    """인증 없는 메인 인터페이스 (기존 방식)"""
    css = """
    .gradio-container {
        width: 70vw !important; 
        max-width: 70% !important; 
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 10px !important;
    }
    .header-text {
        text-align: center;
        margin-bottom: 20px;
    }
    .tab-header-text {
        text-align: center;
    }
    .theme-section {
        margin-bottom: 10px;
        padding: 15px;
        border-radius: 10px;
    }
    """

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

    with gr.Blocks(title="Browser Use WebUI", theme=theme_map[theme_name], css=css, js=js_func) as demo:
        gr.Markdown(
            """
            # 🌐 Browser Use WebUI
            ### Control your browser with AI assistance
            """,
            elem_classes=["header-text"],
        )

        with gr.Tabs():
            with gr.TabItem("⚙️ Agent Settings"):
                create_agent_settings_tab(ui_manager)
            with gr.TabItem("🌐 Browser Settings"):
                create_browser_settings_tab(ui_manager)
            with gr.TabItem("🤖 Run Agent"):
                create_browser_use_agent_tab(ui_manager)
            with gr.TabItem("🎁 Agent Marketplace"):
                gr.Markdown("### Agents built on Browser-Use", elem_classes=["tab-header-text"])
                with gr.Tabs():
                    with gr.TabItem("Deep Research"):
                        create_deep_research_agent_tab(ui_manager)
            with gr.TabItem("📁 Load & Save Config"):
                create_load_save_config_tab(ui_manager)
    
    return demo