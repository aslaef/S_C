'''Szimpla socket kliens nem szabványos egyszerű kéréssel'''
import socket
import sys
import time


class MyshockC:

    def handle_some_data(self, datas):
        print('   handle_some_data: here we can reassemble the requested datas or work with them.... ')


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 4444)
        client_address = ('', 1247)
        sock.bind(client_address)
        print('connecting to %s port %s' % server_address)
        sock.connect(server_address)

        try:
            message = '01'
            print('msg sending')
            sock.send(message.encode())
            print('msg sent\n'
                  'response:')

            # Look for the response
            received_items=0

            expected = int(sock.recv(1024))
            datas = []
            while(received_items<expected):
                data = sock.recv(1024)
                print (data)
                datas.append(data)

                received_items+=1
            self.handle_some_data(datas)
            time.sleep(2)

        finally:
            print('closing connection')
            sock.close()

if __name__ == '__main__':
    ms = MyshockC()
    ms.run()