"""CSS 스타일 정의"""

def get_auth_styles() -> str:
    """인증 관련 CSS 스타일"""
    return """
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


def get_main_styles() -> str:
    """메인 애플리케이션 CSS 스타일"""
    return """
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


def get_combined_styles() -> str:
    """모든 CSS 스타일 결합"""
    return get_auth_styles() + get_main_styles()