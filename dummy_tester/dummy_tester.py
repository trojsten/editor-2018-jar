import os
import json

from django.utils.six.moves import socketserver as SocketServer
from django.utils.six.moves import urllib

protocol_file_names = {
    'ok': 'OK.protocol',
    'all': 'ALL.protocol',
    'cerr': 'CERR.protocol',
}

default_protocol = 'ALL.protocol'


class DummyTester(SocketServer.BaseRequestHandler):
    """
    Depending on filename of submitted file, returns one of three protocols.
    """
    def handle(self):
        input_data = self.request.recv(1024 * 1024).strip()
        print('Connection from: ' + str(self.client_address))
        self.request.close()

        data = json.loads(input_data.decode('UTF-8'))

        submit_id = data['submit_id']

        protocol_file_name = default_protocol

        with open(protocol_file_name, 'rb') as protocol_file:
            protocol_data = protocol_file.read()

        data = urllib.parse.urlencode({
            'submit_id': int(submit_id),
            'protocol': protocol_data
        }).encode('utf-8')
        url = 'http://127.0.0.1:8000/submit/receive_protocol/'

        req = urllib.request.Request(url, data)
        urllib.request.urlopen(req)

if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 12347
    server = SocketServer.TCPServer((HOST, PORT), DummyTester)
    server.serve_forever()
    print('Running!')
