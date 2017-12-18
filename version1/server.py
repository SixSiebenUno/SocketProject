import socket, select

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket: #and in the same chat-room# :
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
    connection_LIST = [] # Connection socket information
    room_dic = [] # Chat-room information
    nickname_dic = [] # User nickname

    MAX_CLIENT = 1024
    RECV_BUFFER = 4096
    PORT = 97127

    server_socket = socket.socket(socket.AF_INET, socet.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(MAX_CLIENT)

    connection_LIST.append(server_socket)
    room_dic[server_socket] = 0
    nickname_dic[server_socket] = "admin"

    
