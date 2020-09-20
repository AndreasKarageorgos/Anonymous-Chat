import socks


class torSocks():

    def __init__(self,link,port):
        self.link = link
        self.port = port
    
    def connect(self):
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
        self.socket = socks.socksocket()
        self.socket.connect((self.link,self.port))
    
    def send(self,text):
        self.socket.sendall(text)
    
    def recv(self,size):
        return self.socket.recv(size)
    
    def setTimeout(self,time):
        self.socket.settimeout(time)

    def close(self):
        self.socket.close()