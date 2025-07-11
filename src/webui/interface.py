import gradio as gr

from src.webui.webui_manager import WebuiManager
from src.webui.auth import create_auth_manager
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


def logout_user():
    """로그아웃 처리 - 페이지 새로고침으로 로그인 화면으로 돌아감"""
    return gr.update(), gr.HTML("""
        <script>
        setTimeout(function() {
            window.location.reload();
        }, 100);
        </script>
        <div style="text-align: center; padding: 20px;">
            <h3>로그아웃 중...</h3>
            <p>잠시 후 로그인 화면으로 이동합니다.</p>
        </div>
    """)


def create_ui(theme_name="Ocean", enable_auth=True):
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

    # dark mode in default
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
            css=css, 
            js=js_func
    ) as demo:
        # 로그아웃 관련 컴포넌트 (숨김)
        logout_trigger = gr.Button("로그아웃", visible=False)
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
                if enable_auth:
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
        if enable_auth:
            logout_btn.click(
                fn=logout_user,
                inputs=[],
                outputs=[logout_trigger, logout_output]
            )
    return demo, enable_auth
