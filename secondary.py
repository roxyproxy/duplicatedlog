from concurrent import futures
from threading import Thread
from flask import Flask
from flask_restful import Resource, Api

import logging
import uuid
import grpc
import duplicatedlog_pb2 as my_pb
import duplicatedlog_pb2_grpc as my_grpc

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

class SecondaryProtocol(my_grpc.ProtocolServicer):
    def replicate(self, request, context):
        log.info(f"Received: {request.message}")
        messages[str(uuid.uuid4())] = request.message
        return my_pb.Response(message="ok")

class MessageApi(Resource):
    def get(self):
        return messages

api.add_resource(MessageApi, '/')
protocol = SecondaryProtocol()
nodeid = uuid.uuid4()
messages = {} 
masterPort = 50051

def add_node():
    log.info("Registering secondary node ...")
    with grpc.insecure_channel("localhost:" + str(masterPort)) as channel:
        stub = my_grpc.ProtocolStub(channel)
        response = stub.register_secondary_node(my_pb.Request(message=str(nodeid)))
    log.info(f"Registered on port: {response.message}")
    return response.message

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc.add_ProtocolServicer_to_server(protocol, server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    log.info(f"Server started, listening on port: {port}")
    server.wait_for_termination()

def web():
    app.run(debug=True, use_reloader=False, port=port)

if __name__ == "__main__":
    port = add_node()
    Thread(target=web).start()
    serve()