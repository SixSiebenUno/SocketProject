import socket, select

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and room_dic.get(socket, 0) == room_dic.get(sock, 0):
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
    CONNECTION_LIST = [] # Connection socket information
    room_dic = {} # Chat-room information
    nickname_dic = {} # User nickname

    MAX_CLIENT = 1024
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(MAX_CLIENT)

    CONNECTION_LIST.append(server_socket)
    room_dic[server_socket] = '0'
    nickname_dic[server_socket] = "admin"

    print "Chat server started on port " + str(PORT)

    index = 0

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    print data
                    if data:
                        if data[0] == '$' and data[-1] == '$':
                            data = data[1:-1]
                            print data
                            key, value = data.split(':')
                            print key, value
                            if key == "nickname":
                                nickname_dic[sock] = value
                            if key == "room":
                                room_dic[sock] = value
                                broadcast_data(sock, "%s entered chat-room %s\n" %(nickname_dic.get(sock), value))
                        else:
                            broadcast_data(sock, "\r" + '<' + nickname_dic.get(sock, sock) + '> ' + data)
                except:
                    broadcast_data(sock, "%s is offline" % nickname_dic.get(sock, sock))
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
