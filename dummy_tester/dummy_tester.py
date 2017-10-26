import os

from django.utils.six.moves import socketserver as SocketServer
from django.utils.six.moves import urllib

protocol_file_names = {
    'ok': 'OK.protocol',
    'all': 'ALL.protocol',
    'cerr': 'CERR.protocol',
}

default_protocol = 'OK.protocol'


class DummyTester(SocketServer.BaseRequestHandler):
    """
    Depending on filename of submitted file, returns one of three protocols.
    """
    def handle(self):
        input_data = self.request.recv(1024 * 1024).strip()
        print('Connection from: ' + str(self.client_address))
        self.request.close()

        data_str = input_data.decode('utf8')
        data_obj = data_str.split('\n', 6)
        submit_id = data_obj[1]

        submit_file_name = data_obj[5]
        submit_type = os.path.splitext(submit_file_name)[0].lower()
        protocol_file_name = protocol_file_names.get(submit_type, default_protocol)

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
