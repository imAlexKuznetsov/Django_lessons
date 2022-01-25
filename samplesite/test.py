import selectors
import socket

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 50005))
    server_socket.listen()
    print('Wait connections...')
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connect on ', addr)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=sent_message)


def sent_message(client_socket):
    request = client_socket.recv(4096)
    response = 'Async server answer'
    if request:

        response = response + '=>' + str(request)
        client_socket.send(response.encode())


def event_loop():
    while True:
        process_ready = selector.select(0.01)
        for sock, _ in process_ready:
            callback = sock.data
            callback(sock.fileobj)


if __name__ == '__main__':
    server()
    event_loop()


