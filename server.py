#!/usr/bin/env python3
"""
Groundwork - local server.

Serves the app on your PC AND to your phone over the same Wi-Fi, so you can
install it to your home screen.

    python server.py

Then open the printed address on your phone's browser.
"""

import os
import socket
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 4100

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet

    def end_headers(self):
        # Never cache during development, so edits show up on a reload.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()

    def guess_type(self, path):
        if path.endswith(".webmanifest") or path.endswith("manifest.json"):
            return "application/manifest+json"
        return super().guess_type(path)


def lan_ip():
    """Best guess at this machine's address on the local network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))      # no packets sent; just picks the route
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


if __name__ == "__main__":
    ip = lan_ip()
    server = HTTPServer(("0.0.0.0", PORT), Handler)

    print("=" * 52)
    print("  Groundwork is running.")
    print()
    print(f"  On this PC:   http://localhost:{PORT}")
    if ip:
        print(f"  On your phone: http://{ip}:{PORT}")
        print("                 (same Wi-Fi network)")
    print("=" * 52)
    print("  Phone: open that address, then use your browser's")
    print("  Share / menu > 'Add to Home Screen'.")
    print()
    print("  (Press Ctrl+C to stop)")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
