import shutil
import tempfile

from httmock import HTTMock

from dyntftpd.handlers.http import HTTPHandler

from . import TFTPServerTestCase


def get_small_file(url, request):
    return 'small file'


def get_404(url, request):
    return {
        'status_code': 404,
        'content': '404 error'
    }


class TestHTTPHandler(TFTPServerTestCase):

    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        return super(TestHTTPHandler, self).setUp(handler=HTTPHandler, handler_args={
            'http': {
                'cache_dir': self.cache_dir
            }
        })

    def tearDown(self):
        shutil.rmtree(self.cache_dir)
        super(TestHTTPHandler, self).tearDown()

    def test_retrieve_file(self):
        with HTTMock(get_small_file) as mock:
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            # \x00\x03 = data
            # \x00\x01 = block id 1
            self.assertEqual(data, '\x00\x03\x00\x01small file')
            self.ack_n(1)

    def test_404(self):
        with HTTMock(get_404) as mock:
            self.get_file('http://www.download.tld/superfile')
            data, _ = self.recv()
            # \x00\x05 = error
            # \x00\x04 = permission denied
            self.assertTrue(data.startswith('\x00\x05\x00\x02'))