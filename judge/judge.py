import os
import sys
import json
import glob
import math

from runners.run_all import MasterRunner
from runners.init_runner import InitRunner

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
        message = result[0]
        line = result[1]
        detailsMsg = result[2]
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

def get_var_str(var):
    if isinstance(var, str):
        # z nejakeho dovodu toto funguje ak string obsahuje znaky \x01
        s = "%s" % [var]
        return s[1:-1]
    return str(var)

def compare(memory, premenna, hodnota, problem):
    variables = load_variables(problem)
    if premenna in variables['FLOATS']:
        return math.isclose(memory[premenna],hodnota, rel_tol=1e-05, abs_tol=0.00001)
    elif premenna in variables['FLOAT_VECTORS']:
        return all(list(map(lambda x:math.isclose(x[0],x[1],rel_tol=1e-05, abs_tol=0.00001), zip(memory[premenna],hodnota))))
    else:
        return hodnota == memory[premenna]


def run_tests(problem, master, protokol):
    runLog = SubElement(protokol, 'runLog')
    count_ok = 0
    skipping = False
    tles = 0
    for i, input_path in enumerate(sorted(glob.glob('test/%s/*.in' % problem))):
        print(input_path)
        message, line, diff = 'OK', 0, {}
        
        if tles >= 2:
            message, line, diff = 'IGN', 0, {}
        else:
            base = os.path.splitext(input_path)[0]
            result = master.run(input_path)
            if isinstance(result, tuple):
                message = result[0]
                line = result[1]
            elif isinstance(result, dict):
                memory = result

                with open('%s.out' % base, 'r') as out_file:
                    output = json.loads(out_file.read())
                    ok = True
                    for premenna, hodnota in output.items():
                        # TODO: floaty su meh
                        if not compare(memory, premenna, hodnota, problem):
                            ok = False
                            diff[premenna] = (hodnota, memory[premenna])
                    if ok:
                        message = 'OK'
                        count_ok += 1
                    else:
                        message = 'WA'

        print("Msg ", message)
        if message == "TLE":
            tles += 1

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
                s += 'nas %s: %s\n' % (premenna, get_var_str(nasa))
                s += 'tvoj %s: %s' % (premenna, get_var_str(tvoja))
                s += '\n'
            details.text = s
    score = SubElement(runLog, 'score')
    score.text = str(count_ok)


def load_variables(problem):
    variables_file = glob.glob('test/%s/variables.json' % problem)
    if len(variables_file) == 0:
        return None
    else:
        return json.load(open(variables_file[0]))


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
        user_id = data['user_id']
        print('Handling submit:', submit_id, ' problem:', problem, ' custom:', custom, ' user:', user_id)

        protokol = Element('protokol')

        os.makedirs('submits/%s/' % submit_id)

        with open('submits/%s/data.code' % submit_id, 'w') as out:
            for content, lang in code:
                out.write('%s: %s\n' % (lang, content))

        master = MasterRunner(code, prefix=str(submit_id), variables=load_variables(problem))
        result = master.prepare()
        if result is not None:
            add_compile(protokol, result)
        elif not custom:
            run_tests(problem, master, protokol)
        else:
            input_path = 'submits/%s/data.custom' % submit_id
            init = InitRunner(variables=load_variables(problem), codename=str(submit_id))
            init.prepare_memory(custom_input, input_path)
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
    HOST, PORT = '0.0.0.0', 12347
    if len(sys.argv) >= 2:
        PORT = int(sys.argv[1])
    server = SocketServer.TCPServer((HOST, PORT), EditorJudge)
    print('Running on %s:%s' % (HOST, PORT))
    server.serve_forever()
