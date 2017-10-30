import os
import json
import glob

from runners.run_all import MasterRunner
from runners.runner import InitRunner

from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from django.utils.six.moves import socketserver as SocketServer
from django.utils.six.moves import urllib

def add_compile(protokol, result):
    # result: None alebo (CERR, line_number, msg)
    compileLog = SubElement(protokol, 'compileLog')
    compileLog.text = result[2]
    lineNumber = SubElement(protokol, 'cLogLineNumber')
    lineNumber.text = str(result[1])

def run_tests(problem, master, protokol):
    runLog = SubElement(protokol, 'runLog')
    for input_path in glob.glob('test/%s/*.in' % problem):
        base = os.path.splitext(input_path)[0]
        result = master.run(input_path)
        message = 'OK'
        line = 0
        if isinstance(result, tuple):
            message = 'EXC'
            line = result[1]
        elif isinstance(result, dict):
            memory = result

            with open('%s.out' % base, 'r') as out_file:
                output = json.loads(out_file.read())
                ok = True
                for premenna, hodnota in output.items():
                    if hodnota != memory[premenna]:
                        ok = False
                        break
                if ok:
                    message = 'OK'
                else:
                    message = 'WA'

        # crete xml elements
        test = SubElement(runLog, 'test')
        name = SubElement(test, 'name')
        resultMsg = SubElement(test, 'resultMsg')
        lineNumber = SubElement(test, 'lineNumber')
        #details = SubElement(test, 'details') # TODO: add details
        name.text = os.path.basename(input_path)
        resultMsg.text = message
        lineNumber.text = str(line)

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

        master = MasterRunner(code)
        result = master.prepare()
        if result is not None:
            add_compile(protokol, result)
        else:
            run_tests(problem, master, protokol)

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
