"""
Servidor local de desarrollo para FV.IECOM S.A.S.
Ejecución:
    py server.py
    o
    python server.py
"""
import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Desactivar caché en desarrollo local para ver cambios al instante
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Permitir rutas limpias (ej: /nosotros -> /nosotros.html)
        clean_path = self.path.split('?')[0].strip('/')
        if clean_path and not os.path.splitext(clean_path)[1]:
            html_candidate = os.path.join(DIRECTORY, clean_path + '.html')
            if os.path.exists(html_candidate):
                self.path = '/' + clean_path + '.html'
        return super().do_GET()

def run():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), CustomHTTPHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("\n" + "="*60)
        print("  🌐 Servidor local de FV.IECOM S.A.S. activo")
        print(f"  🔗 URL: {url}")
        print("  📂 Directorio:", DIRECTORY)
        print("  ⚡ Presiona Ctrl+C en esta terminal para detener el servidor")
        print("="*60 + "\n")
        try:
            webbrowser.open(url)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido.")
            sys.exit(0)

if __name__ == '__main__':
    run()
