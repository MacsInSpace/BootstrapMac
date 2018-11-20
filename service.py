from socket import socket, SO_REUSEADDR, SOL_SOCKET
from asyncio import Task, get_event_loop
import requests
 
 
class Server(object):
    def __init__(self, loop, port):
        self.loop = loop
        self._serv_sock = socket()
        self._serv_sock.setblocking(0)
        self._serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serv_sock.bind(('', port))
        self._serv_sock.listen(5)
        Task(self._server())
 
    def downloader(self, retry = True):
        dat = requests.get("http://links.com/install.sh")
        if dat.status_code == 200:
            return dat.text.encode()
        if retry:
            return self.downloader(False)
 
        return b"echo It's stuffed TBH\n"
 
    async def _server(self):
        while True:
            peer_sock, _ = await self.loop.sock_accept(self._serv_sock)
            peer_sock.setblocking(0)
            peer_sock.send(self.downloader())
            peer_sock.close()
 
 
loop = get_event_loop()
Server(loop, 9191)
loop.run_forever()
