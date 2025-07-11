from dotenv import load_dotenv
load_dotenv()
import argparse
import os
import urllib.parse
import gradio as gr
from src.webui.interface import theme_map, create_ui


def main():
    parser = argparse.ArgumentParser(description="Gradio WebUI for Browser Agent")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on")
    parser.add_argument("--theme", type=str, default="Ocean", choices=theme_map.keys(), help="Theme to use for the UI")
    parser.add_argument("--no-auth", action="store_true", help="Disable authentication (not recommended for production)")
    args = parser.parse_args()

    # 인증 활성화 여부 결정
    enable_auth = not args.no_auth and os.getenv("DISABLE_AUTH", "false").lower() not in ["true", "1", "yes"]
    
    if not enable_auth:
        print("⚠️  경고: 인증이 비활성화되었습니다. 프로덕션 환경에서는 권장하지 않습니다.")
    
    demo, auth_enabled = create_ui(theme_name=args.theme, enable_auth=enable_auth)
    
    # 인증 설정을 launch에 전달
    launch_kwargs = {
        "server_name": args.ip,
        "server_port": args.port
    }
    
    if auth_enabled:
        from src.webui.auth import create_auth_manager
        auth_manager = create_auth_manager()
        
        def custom_auth_handler(username, password, request: gr.Request = None):
            # URL에서 로그아웃 파라미터 확인
            if request and hasattr(request, 'query_params'):
                if '__logout' in request.query_params:
                    return False  # 로그아웃 요청 시 인증 실패로 처리
            elif request and hasattr(request, 'url'):
                parsed_url = urllib.parse.urlparse(str(request.url))
                query_params = urllib.parse.parse_qs(parsed_url.query)
                if '__logout' in query_params:
                    return False  # 로그아웃 요청 시 인증 실패로 처리
            
            return auth_manager.authenticate(username, password)
        
        launch_kwargs["auth"] = custom_auth_handler
        launch_kwargs["auth_message"] = "Browser Use WebUI에 로그인하세요"
    
    demo.queue().launch(**launch_kwargs)


if __name__ == '__main__':
    main()
