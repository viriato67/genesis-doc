import sys
import os
import threading
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CONTENT = open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"),
    encoding="utf-8"
).read() if not getattr(sys, "frozen", False) else None

# When packaged by PyInstaller, embed the HTML inline
EMBEDDED_HTML = None  # replaced at build time via --add-data

def get_html():
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle
        base = sys._MEIPASS
        path = os.path.join(base, "index.html")
        with open(path, encoding="utf-8") as f:
            return f.read()
    return HTML_CONTENT

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = get_html()
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass  # suppress server logs

def find_free_port():
    import socket
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def main():
    port = find_free_port()
    server = HTTPServer(("127.0.0.1", port), Handler)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    time.sleep(0.3)  # let server start
    url = f"http://127.0.0.1:{port}"

    # Try to open in app mode (no address bar) — Chrome/Edge
    opened = False
    for browser_cmd in [
        "google-chrome",
        "chromium-browser",
        "chromium",
        "microsoft-edge",
        "msedge",
    ]:
        try:
            import subprocess
            subprocess.Popen(
                [browser_cmd, f"--app={url}", "--disable-extensions"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            opened = True
            break
        except FileNotFoundError:
            continue

    if not opened:
        webbrowser.open(url)

    # Keep alive until user closes terminal / process
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()
