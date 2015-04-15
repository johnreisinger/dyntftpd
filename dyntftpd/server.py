import SocketServer

from .handlers.clever import CleverHandler


class TFTPServer(SocketServer.UDPServer):
    """ Accepts the same arguments than SocketServer.UDPServer.

    Can also provide `handler_args`, a dictionary used by handlers to lookup
    their configuration.
    """
    def __init__(self, host='', port=69, root='/var/lib/tftpboot',
                 handler=CleverHandler, handler_args=None):

        self.sessions = {}
        self.root = root
        self.handler_args = handler_args or {}
        SocketServer.UDPServer.__init__(self, (host, port), handler)
