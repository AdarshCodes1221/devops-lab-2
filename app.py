import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Core Distributed Media Transcoder Microservice - OTT Video Streaming Platform
PORT = int(os.environ.get("PORT", 80))
CONFIG_PATH = os.environ.get("TRANSCODE_CONF", "transcode.conf")

def read_config():
    conf = {"max_bitrate": "4k", "engine": "ffmpeg-cluster", "preset": "veryfast"}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        conf[k.strip().lower()] = v.strip()
        except Exception as e:
            print(f"[WARN] Error reading {CONFIG_PATH}: {e}")
    return conf

class TranscoderHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conf = read_config()
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "media-transcoder-engine"}).encode("utf-8"))
        elif self.path == "/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(conf).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            response_text = f"transcoder engine ready\nService: OTT Media Transcoder v5.0.0\nMax Bitrate: {conf.get('max_bitrate', '4k')}\n"
            self.wfile.write(response_text.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def run():
    # Print the exact required verification string to stdout for Docker and terminal logs
    print("transcoder engine ready", flush=True)
    conf = read_config()
    print(f"[*] OTT Media Transcoder Service v5.0.0 initialized with max_bitrate={conf.get('max_bitrate', '4k')}", flush=True)
    print(f"[*] Listening on port {PORT}...", flush=True)
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, TranscoderHTTPHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down transcoder engine...")
        httpd.server_close()

if __name__ == "__main__":
    run()