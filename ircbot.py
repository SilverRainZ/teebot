# -*- encoding: UTF-8 -*-
# simple ircbot
import re
import socket

class ircbot:
    sock = None
    chans = []

    def __init__(self, host, port, nick):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(20)
        self.sock.connect((host, port))

        self.sock.send(bytes('NICK ' + nick + '\n', 'utf-8'))
        self.sock.send(bytes('USER ' + nick + ' ' + nick + ' ' + nick + ' :' + nick + '\n', 'utf-8'))
        print('[ircbot]', 'connect to {0}:{1}'.format(host, port))


    def join_chan(self, chan):
        self.sock.send(bytes('JOIN ' + chan + '\n', 'utf-8'))
        self.chans.append(chan)
        print('[ircbot]', 'join', chan)


    def ping(self):
        print('[ircbot]', 'ping!')
        self.sock.send(bytes('PONG :pingis\n', 'utf-8'))


    def send_msg(self, chan, msg):
        try:
            self.sock.send(bytes('PRIVMSG ' + chan + ' :' + msg + '\n','utf-8'))
        except socket.error as err:
            print('[ircbot]', 'err: ', 'SOCKET ERROR', err)
        else:
            print('[ircbot]', 'send to {0}: {1}'.format(chan, msg))


    def recv_msg(self):
        try:
            msg_pattern = re.compile(r':(.*?)!~.*?@.*? PRIVMSG (.*?) :(?u)(.*)')

            data = self.sock.recv(2048)
            data = data.decode('utf-8').strip('\n\r')
            if (data.startswith('PING')):  # keep alive
                self.ping()
            msg_info = msg_pattern.match(data)
            if msg_info:
                man, chan, msg = msg_info.groups()
                print('[ircbot]', 'recv msg: {0}@{1}: {2}'.format(man, chan, msg))
                return (man, chan, msg)

        except socket.error as err:
            print('[ircbot]', 'err: ', 'SOCKET ERROR', err)
        except UnicodeDecodeError as err:
            print('[ircbot]', 'err: ', 'DECODE ERROR', err)
        except re.error as err:
            print('[ircbot]', 'err: ', 'MATCH ERROR', err)

        return (None, None, None)


    def stop(self):
        print('[ircbot]', 'stop')
        self.sock.close()
