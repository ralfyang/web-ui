from dotenv import load_dotenv
load_dotenv()
import argparse
import os
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
    
    demo = create_ui(theme_name=args.theme, enable_auth=enable_auth)
    demo.queue().launch(server_name=args.ip, server_port=args.port)


if __name__ == '__main__':
    main()
