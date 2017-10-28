import os
import json
import glob

from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from django.utils.six.moves import socketserver as SocketServer
from django.utils.six.moves import urllib

def add_compile(protokol, result):
    # result: None alebo (msg, line_number, return_code)
    # TODO: add line information
    compileLog = SubElement(protokol, 'compileLog')
    compileLog.text = result[0]

def run_tests(protokol, problem, code):
    # TODO: actually run something
    runLog = SubElement(protokol, 'runLog')
    for file_path in glob.glob('test/%s/*.in' % problem):
        test = SubElement(runLog, 'test')
        name = SubElement(test, 'name')
        resultMsg = SubElement(test, 'resultMsg')
        #details = SubElement(test, 'details') # TODO: add details
        name.text = os.path.basename(file_path)
        resultMsg.text = 'OK' # change to read answer

class EditorJudge(SocketServer.BaseRequestHandler):
    def handle(self):
        input_data = self.request.recv(1024 * 1024).strip()
        print('Connection from: ' + str(self.client_address))
        self.request.close()

        data = json.loads(input_data.decode('UTF-8'))
        submit_id = data['submit_id']
        problem = data['problem']
        code = data['code']

        protokol = Element('protokol')

        # TODO: really compile
        # None alebo (msg, line_number, return_code)
        result = ("fskebvskeve", 5, 0)
        result = None
        if result is not None:
            add_compile(protokol, result)
        else:
            run_tests(protokol, problem, code)

        protocol_data = tostring(protokol)

        data = urllib.parse.urlencode({
            'submit_id': int(submit_id),
            'protocol': protocol_data
        }).encode('utf-8')
        url = 'http://127.0.0.1:8000/submit/receive_protocol/'

        req = urllib.request.Request(url, data)
        urllib.request.urlopen(req)

if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 12347
    server = SocketServer.TCPServer((HOST, PORT), EditorJudge)
    server.serve_forever()
    print('Running!')
