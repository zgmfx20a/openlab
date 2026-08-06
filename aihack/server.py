#!/usr/bin/env python3
"""
簡易HTTPサーバー起動スクリプト
ASI DIVE 薬物配送ミッション用
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# 設定
PORT = 8000
HOST = "localhost"

# コマンドライン引数でポートを指定可能: python3 server.py [ポート番号]
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"⚠️  ポート番号の指定が不正です: {sys.argv[1]}（既定の {PORT} を使います）")

# プロジェクトルートに移動
os.chdir(Path(__file__).parent)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS対応（開発用）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    GAME_FILE = "medicine-delivery.html"
    
    # サーバーを先にバインド（ポートが使用中なら自動で次へ）
    global PORT
    port = PORT
    while True:
        try:
            httpd = socketserver.TCPServer((HOST, port), MyHTTPRequestHandler)
            PORT = port
            break
        except OSError as e:
            if e.errno == 98 and port < 65000:
                print(f"⚠️  ポート {port} は使用中です。ポート {port + 1} に切り替えます")
                port += 1
            else:
                raise
    
    print("=" * 60)
    print("ASI DIVE 薬物配送ミッション - ローカルWebサーバー")
    print("=" * 60)
    print(f"\n🌐 サーバーを起動しています...")
    print(f"   URL: http://{HOST}:{PORT}/{GAME_FILE}")
    print(f"   ポート: {PORT}")
    print(f"\n📁 カレントディレクトリ: {os.getcwd()}")
    
    # 必要なファイルをチェック
    required_files = [
        GAME_FILE,
        "gvrm/sample5.gvrm",
        "fbx/Idle.fbx",
        "fbx/Fast Run.fbx",
        "fbx/Shrugging.fbx",
        "backsound/backsound.mp3"
    ]
    
    print("\n✓ ファイルチェック:")
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (見つかりません)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  警告: {len(missing_files)}個のファイルが見つかりません")
    
    print("\n" + "=" * 60)
    print("サーバーが起動しました！")
    print("ブラウザで以下のURLにアクセスしてください：")
    print(f"👉 http://{HOST}:{PORT}/{GAME_FILE}")
    print("\n終了するには Ctrl+C を押してください")
    print("=" * 60 + "\n")
    
    # ブラウザを自動で開く（オプション）
    try:
        webbrowser.open(f"http://{HOST}:{PORT}/{GAME_FILE}")
        print("✓ ブラウザを開きました\n")
    except:
        print("⚠️  ブラウザの自動起動に失敗しました（手動でURLを開いてください）\n")
    
    # サーバー起動
    with httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 サーバーを停止しています...")
            print("✓ サーバーが正常に終了しました\n")

if __name__ == "__main__":
    main()

