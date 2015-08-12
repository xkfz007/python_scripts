# This is a simple file read server
from SimpleXMLRPCServer import SimpleXMLRPCServer

def file_reader(file_name):
    with open(file_name, 'r') as f:
        return f.read()

#server = SimpleXMLRPCServer(('localhost', 8001))
server = SimpleXMLRPCServer(('172.21.40.170', 8001))
server.register_introspection_functions()
server.register_function(file_reader)
server.serve_forever() 