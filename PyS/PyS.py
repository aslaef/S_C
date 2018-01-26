'''Szimpla socket szerver néhány egyszerű üzenettel, + xls példányosítás'''
from xlrd import open_workbook
import socket
import sys
import time

#Xls 1 sora:
class xlsObject:
    def __init__(self, id, name, weight):
        self.id=id
        self.name=name
        self.weight=weight

    def coded(self):
        return str(self.id)+" ; "+str(self.name)+" ; "+str(self.weight)

#schocket server:
class Myshock:

    #xls beolvasása és sorok példányosítása
    def wbhandler(self):
        wb = open_workbook('some.xlsx')

        for sheet in wb.sheets():
            number_of_rows = sheet.nrows
            number_of_columns = sheet.ncols

            items = []

            rows = []
            for row in range(1, number_of_rows):
                values = []
                for col in range(number_of_columns):
                    value = (sheet.cell(row, col).value)

                    try:
                        value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        values.append(value)

                item = xlsObject(*values)
                items.append(item)
        #visszaadja a beolvasott példányokat
        return items


    def setup(self):
        #szerver socket:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address=('', 4444)
        print('binding')

        sock.bind(server_address)
        sock.listen(1)
        #beérkező kapcsolat, üzenet:
        while (True):
            print('==============================================')
            connection, client_address= sock.accept()
            #ez a kapcsolt kliens címe:
            print(client_address)

            try:
                print('receiving:')
                not_sent=True
                while(not_sent):

                    datain=connection.recv(1024)
                    #datain: a beérkező üzenet kódolt formában
                    if(datain):
                        #ez az üzenet:
                        d=datain.decode()
                        print('incoming msg:'+d)
                        #ha az üzenet 01 es kódú akkor az az xls tábla lekérésére vonatkozik --- ellenkező esetben visszatér egy 'invalid request üzenet'
                        if(d=='01'):
                            print('sending data back to the client')
                            #xls lekérés és feldolgozás:
                            itemstosend = self.wbhandler()
                            #ennyi darab objektumunk van... ezt előre jelezzük hogy ennyi üzenet fog érkezni
                            connection.sendall(str(len(itemstosend)).encode())
                            #xls objektumok visszabontása stringekké és a stringek dekódolt továbbítása a szervernek
                            for item in itemstosend:
                                print('sending one item...')
                                connection.sendall(item.coded().encode())

                        #ha az üzenet nem 01-es kódú a szerver nem ismeri fel (ez fejlesztehtő egy egyszerű kódtáblával(pl '01': request_xls ...) több fajta üzenet esetén aminek célja az üzenet hosszának le redukálása)
                        else:connection.sendall("invalid request".encode())
                        not_sent = False

                    time.sleep(2)

            finally:
                print('closing connection')

                connection.close()
        print('_______________')
        time.sleep(1)



if __name__ == "__main__":
    ms = Myshock()
    ms.setup()

