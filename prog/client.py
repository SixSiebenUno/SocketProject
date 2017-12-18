import socket, select, string, sys

def prompt():
    sys.stdout.write("<%s> " % nickname)
    sys.stdout.flush()

if __name__ == "__main__":

    RECV_BUFFER = 4096

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print 'Unable to connect' # Waiting to change
        sys.exit()

    print 'Connected to remote host...' # Waiting to change

    nickname = "You"
    roomno = '0'

    sys.stdout.write("Please set your nickname : ")
    nickname = sys.stdin.readline()
    nickname = nickname[0:-1]

    sys.stdout.write("Enter your chatroom number : ")
    roomno = sys.stdin.readline()
    roomno = roomno[0:-1]

    msg = '$nickname:' + nickname + '$'
    print msg
    s.send(msg)

    msg = '$room:' + roomno + '$'
    print msg
    s.send(msg)

    prompt()

    rlist = [sys.stdin, s]

    while 1:
        read_list, write_list, error_list = select.select(rlist , [], [])
        for sock in read_list:
            if sock == s:
                data = sock.recv(RECV_BUFFER)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
