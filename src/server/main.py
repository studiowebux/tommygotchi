import http.server
import socketserver
import json
import whisper
import re
import os

PORT = 4242

class APIHandler(http.server.SimpleHTTPRequestHandler):
    model = whisper.load_model("medium")
    
    def transcribe(self, path):
        result = self.model.transcribe(path)
        print(result)
        return result["text"]
    
    def process_file(self):
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        filename = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not filename:
            return (False, "Can't find out file name...")
        filename = os.path.join("uploads", filename[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)

        try:
            out = open(filename, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, filename)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")
    
    def do_POST(self):
        r, filename = self.process_file()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        transcribed = self.transcribe(filename)
        
        if r == True:
            os.remove(filename)
            output_data = {'status': 'OK', 'result': transcribed}
        else:
            output_data = {'status': 'ERR', 'result': "Failed to transcribe..."}
        output_json = json.dumps(output_data)
        
        print(output_json.encode('utf-8'))
        self.wfile.write(output_json.encode('utf-8'))


Handler = APIHandler

try:
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting http://0.0.0.0:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping by Ctrl+C")
    httpd.server_close()