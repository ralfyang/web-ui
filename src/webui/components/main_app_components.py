import gradio as gr
from src.webui.webui_manager import WebuiManager
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import create_browser_use_agent_tab
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab


def create_main_application(ui_manager: WebuiManager, logout_button: gr.Button) -> None:
    """메인 애플리케이션 UI 생성"""
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
            # 로그아웃 버튼을 여기에 배치 (render() 제거)
            logout_button

    with gr.Tabs():
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