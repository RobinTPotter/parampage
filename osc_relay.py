"""
HTTP-to-OSC relay for parampage/index.html.

Serves index.html (and other static files) and accepts POSTs to /osc,
forwarding them as real OSC/UDP packets. Serving the page itself means
requests to /osc are same-origin, avoiding CORS entirely.

Run: python osc_relay.py [http_port]
Then open http://localhost:12340/index.html
"""
import json
import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

from osc_ref import send_osc


class OscRelayHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path != "/osc":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
            ip = payload["ip"]
            port = int(payload["port"])
            address = payload["address"]
            args = payload.get("args", [])
            send_osc(ip, port, address, args)
            status, response = 200, {"ok": True}
        except Exception as e:
            status, response = 400, {"ok": False, "error": str(e)}

        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"[osc_relay] {format % args}")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12340
    server = HTTPServer(("localhost", port), OscRelayHandler)
    print(f"OSC relay + web server listening on http://localhost:{port}")
    server.serve_forever()

