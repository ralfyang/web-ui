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
    .user-info {
        text-align: right;
        margin-bottom: 10px;
        padding: 10px;
        background-color: var(--background-fill-secondary);
        border-radius: 8px;
        font-size: 14px;
    }
    .logout-button {
        margin-left: 10px;
        background: #ff4444 !important;
        color: white !important;
        border: none !important;
        padding: 5px 10px !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        text-decoration: none !important;
    }
    .logout-button:hover {
        background: #cc3333 !important;
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
        # 사용자 정보 및 로그아웃 섹션 (인증이 활성화된 경우에만 표시)
        if enable_auth:
            with gr.Row():
                with gr.Column(scale=3):
                    pass  # 빈 공간
                with gr.Column(scale=1):
                    user_info = gr.HTML(
                        value='''
                        <div class="user-info">
                            👤 로그인됨 
                            <button onclick="logout()" class="logout-button">🚪 로그아웃</button>
                        </div>
                        <script>
                        function logout() {
                            if (confirm('정말 로그아웃하시겠습니까?')) {
                                // 세션 스토리지와 로컬 스토리지 클리어
                                sessionStorage.clear();
                                localStorage.clear();
                                
                                // 쿠키 클리어 (Gradio 인증 관련)
                                document.cookie.split(";").forEach(function(c) { 
                                    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
                                });
                                
                                // 페이지 새로고침으로 로그인 화면으로 돌아가기
                                window.location.reload();
                            }
                        }
                        </script>
                        ''',
                        elem_classes=["user-info"]
                    )
        
        with gr.Row():
            gr.Markdown(
                """
                # 🌐 Browser Use WebUI
                ### Control your browser with AI assistance
                """,
                elem_classes=["header-text"],
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

    return demo, enable_auth
