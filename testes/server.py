from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import urllib.parse
import json

class CustomRequestHandler(SimpleHTTPRequestHandler):
    # Dicionário que mapeia as rotas para os diretórios correspondentes
    routes = {
        '/D:/MEDIA/COMERCIAIS': 'D:/MEDIA/COMERCIAIS',
        '/D:/MEDIA/MÚSICAS': 'D:/MEDIA/MÚSICAS',
        '/D:/MEDIA/MÚSICAS/Hits Sertanejo': 'D:/MEDIA/MÚSICAS/Hits Sertanejo',
        '/D:/MEDIA/MÚSICAS': 'D:/MEDIA/MÚSICAS',
        '/D:/': 'D:/',
        '/D:/MEDIA/MÚSICAS': 'D:/MEDIA/MÚSICAS',
        '/D:/MEDIA/MÚSICAS': 'D:/MEDIA/MÚSICAS',
    }

    def do_GET(self):
        # Log da solicitação de caminho
        print("Request path:", self.path)
        # Decodifica a URL para obter o caminho correto
        path = urllib.parse.unquote(self.path)
        # Log do caminho processado
        print("Processed path:", path)
        # Obtém o diretório correspondente ao caminho da solicitação
        root = self.get_root_from_path(path)
        # Verifica se o diretório existe e se é um diretório ou um arquivo
        if root is not None and os.path.exists(root):
            self.directory = root
            print("Serving from directory:", self.directory)
            # Se for um diretório, lista os arquivos no diretório
            if os.path.isdir(root):
                try:
                    # Tenta servir a lista de arquivos no diretório
                    self.send_response(200)
                    # self.send_header("Content-type", "text/html; charset=utf-8")
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(self.list_directory_json(self.directory, path).encode())
                except OSError:
                    # Se houver um erro ao listar o diretório, retorna um erro 404
                    self.send_error(404, "Directory listing failed")
            else:
                # Se for um arquivo, serve o arquivo diretamente
                try:
                    with open(root, 'rb') as file:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/octet-stream')
                        self.end_headers()
                        self.wfile.write(file.read())
                except IOError:
                    self.send_error(404, "File not found")
        else:
            # Se o diretório não existir, retorna um erro 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def get_root_from_path(self, path):
        # Obtém o diretório correspondente à rota
        for route, root in self.routes.items():
            if path.startswith(route):
                file_path = path.replace(route, root, 1)
                if os.path.exists(file_path):
                    return file_path
        return None
    
    def list_directory_json(self, path, relative_path):
        try:
            list = os.listdir(path)
            list.sort(key=lambda a: a.lower())
            # return json.dumps({"files": list})
        except OSError:
            self.send_error(404, "Directory listing failed")
            return None
        
        files = {
            "path": "",
            "files": []
        }
        try:
            files['path'] = path
            for name in list:
                fullname = os.path.join(path, name)
                displayname = linkname = name
                isFolder = 0
                # Adiciona "/" para diretórios
                if os.path.isdir(fullname):
                    displayname = name + '/'
                    linkname = name + '/'
                    isFolder = 1

                files['files'].append({
                    "title": displayname,
                    "link": os.path.join(relative_path, linkname),
                    "type": isFolder
                })
        except Exception as e:
            print("Error:", e)

        return json.dumps(files)


def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8000):
    # Inicia o servidor HTTP
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
