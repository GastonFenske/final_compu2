import sys, os, dotenv
sys.path.append('.')
sys.path.append('service')
from server import Server

dotenv.load_dotenv()

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')

server = Server(SERVER_HOST, SERVER_PORT)
server.start()
