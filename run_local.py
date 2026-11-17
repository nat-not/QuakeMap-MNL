"""Open the educational web project locally with Python's standard library."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os, webbrowser

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
port = 8080
for number in range(8080, 8090):
    try:
        server = ThreadingHTTPServer(('127.0.0.1', number), SimpleHTTPRequestHandler)
        port = number
        break
    except OSError:
        continue
else:
    raise SystemExit('Could not find an available local port (8080–8089).')
url = f'http://localhost:{port}'
print(f'QuakeMap MNL running at {url} — press Ctrl+C to stop.')
webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nStopped.')
finally:
    server.server_close()
