import socket
sock = socket.socket()
sock.bind(('localhost',8000))
sock.listen(1)
bufferSize = 1024

while True:
    connection, addres = sock.accept()  
    buffer = connection.recv(bufferSize).decode(encoding='UTF-8')   
    path = buffer.split('\n')[0].split(' ')[1]
    path = path[1:]
    if(path == ""):
        path ="index.html"
    file = open(path)
    connection.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n' + file.read().encode(encoding='UTF-8'))
    file.close()
    connection.close()
sock.close()
