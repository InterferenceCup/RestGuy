import pickle
import sys


def DynamicSend(sock, SendData):
    Error = 0
    while True:
        try:
            sock.send(SendData)
        except:
            # print("Problem with send")
            Error = 1
            break
        try:
            packet = sock.recv(1024)
        except:
            print("Problem with recv")
            Error = 2
            break
        try:
            if int(str(packet.decode('utf-8'))) == sys.getsizeof(SendData):
                sock.send("YES".encode('utf-8'))
                break
            else:
                sock.send("NO".encode('utf-8'))
        except:
            print("Problem with data")
            Error = 3
            break
    return Error


def DynamicRecv(sock):
    try:
        while True:
            packet = sock.recv(1024)
            data = packet
            sock.send(str(sys.getsizeof(data)).encode('utf-8'))
            packet = sock.recv(1024)
            if str(packet.decode('utf-8')) == "YES":
                break
    except:
        data = None
    return data


def Accept(Sock, Players, String, Map):
    Client, Address = Sock.accept()  # Accept socket
    print("Connected to", Address)  # Print to console
    DynamicSend(Client, String.encode('utf-8'))  # Send name
    DynamicSend(Client, pickle.dumps(Players))  # Send position
    DynamicSend(Client, Map.encode('utf-8'))
    return Client, Address  # Return new address
