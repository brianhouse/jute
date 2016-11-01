import serial, threading, time, os, socket, queue
from housepy import config, log, util


class Receiver(threading.Thread):

    def __init__(self, port=23232, message_handler=None,):
        super(Receiver, self).__init__()
        self.daemon = True
        self.messages = queue.Queue()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('', port))
        except Exception as e:
            log.error(log.exc(e))
            return
        self.start()

    def run(self):
        while True:
            try:
                message, address = self.socket.recvfrom(1024)
                self.messages.put(message.decode())
            except Exception as e:
                log.error(log.exc(e))


class Sender(threading.Thread):

    def __init__(self, port=23232):
        super(Sender, self).__init__()
        self.daemon = True
        self.port = port
        self.messages = queue.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)
        self.start()

    def run(self):
        while True:
            try:
                message, address = self.messages.get(), ("localhost", self.port)
                log.info("SENDING [%s] to %s:%s" % (message, address[0], address[1]))
                self.socket.sendto(message.encode(), address)
            except Exception as e:
                log.error(log.exc(e))

    def send(self, message, address):
        self.messages.put((message, address))
