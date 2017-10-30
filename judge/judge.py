import os
import json
import glob

from runners.run_all import MasterRunner, prepare_memory
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

def run_custom(master, protokol, input_path):
    runLog = SubElement(protokol, 'runLog')

    base = os.path.splitext(input_path)[0]
    result = master.run(input_path)
    message, line, detailsMsg = 'OK', 0, ''
    if isinstance(result, tuple):
        message = 'EXC'
        line = result[1]
    elif isinstance(result, dict):
        memory = result
        message = 'DONE'
        detailsMsg = 'Memory:\n'
        for premenna, hodnota in memory.items():
            detailsMsg += '%s: %s\n' % (premenna, hodnota)

    # crete xml elements
    test = SubElement(runLog, 'test')
    name = SubElement(test, 'name')
    resultMsg = SubElement(test, 'resultMsg')
    lineNumber = SubElement(test, 'lineNumber')
    name.text = 'custom'
    resultMsg.text = message
    lineNumber.text = str(line)
    details = SubElement(test, 'details')
    details.text = detailsMsg

def run_tests(problem, master, protokol):
    runLog = SubElement(protokol, 'runLog')
    count_ok = 0
    for input_path in glob.glob('test/%s/*.in' % problem):
        base = os.path.splitext(input_path)[0]
        result = master.run(input_path)
        message, line, diff = 'OK', 0, {}
        if isinstance(result, tuple):
            message = 'EXC'
            line = result[1]
        elif isinstance(result, dict):
            memory = result

            with open('%s.out' % base, 'r') as out_file:
                output = json.loads(out_file.read())
                ok = True
                for premenna, hodnota in output.items():
                    # TODO: floaty su meh
                    if hodnota != memory[premenna]:
                        ok = False
                        diff[premenna] = (hodnota, memory[premenna])
                if ok:
                    message = 'OK'
                    count_ok += 1
                else:
                    message = 'WA'

        # crete xml elements
        test = SubElement(runLog, 'test')
        name = SubElement(test, 'name')
        resultMsg = SubElement(test, 'resultMsg')
        lineNumber = SubElement(test, 'lineNumber')
        name.text = os.path.basename(input_path)
        resultMsg.text = message
        lineNumber.text = str(line)
        if len(diff) > 0:
            details = SubElement(test, 'details')
            s = ''
            for premenna, (nasa, tvoja) in diff.items():
                s += 'nas %s: %s\n' % (premenna, nasa)
                s += 'tvoj %s: %s\n' % (premenna, tvoja)
            details.text = s
    score = SubElement(runLog, 'score')
    score.text = str(count_ok)

class EditorJudge(SocketServer.BaseRequestHandler):
    def handle(self):
        input_data = self.request.recv(1024 * 1024).strip()
        print('Connection from: ' + str(self.client_address))
        self.request.close()

        data = json.loads(input_data.decode('UTF-8'))
        submit_id = data['submit_id']
        problem = data['problem']
        code = data['code']
        custom = data['custom']
        custom_input = data['custom_input']

        protokol = Element('protokol')

        os.makedirs('submits/%s/' % submit_id)

        with open('submits/%s/data.code' % submit_id, 'w') as out:
            for content, lang in code:
                out.write('%s: %s\n' % (lang, content))

        master = MasterRunner(code, prefix=str(submit_id))
        result = master.prepare()
        if result is not None:
            add_compile(protokol, result)
        elif not custom:
            run_tests(problem, master, protokol)
        else:
            print(custom_input)
            print(json.loads(custom_input))
            input_path = 'submits/%s/data.custom' % submit_id
            prepare_memory(json.loads(custom_input), input_path)
            run_custom(master, protokol, input_path)

        protocol_data = tostring(protokol)

        with open('submits/%s/data.protocol' % submit_id, 'w') as out:
            out.write('%s' % protocol_data)

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
