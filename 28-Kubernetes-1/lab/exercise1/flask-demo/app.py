from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    host    = socket.gethostname()     # to get the hostname
    ip      = socket.gethostbyname(host) # to get the host ip 
    message = os.getenv('MESSAGE', 'Flask Demo')
    return '{} on host {} ({})'.format(message, host, ip)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')