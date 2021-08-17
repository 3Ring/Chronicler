from project.__init__ import create_app
# import eventlet

app = create_app()

# if __name__ == '__main__':
#     SERVER_HOST = ''
#     SERVER_PORT = 5000
#     eventlet.wsgi.server(eventlet.listen(
#             (SERVER_HOST, SERVER_PORT)), create_app()) 