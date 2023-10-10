from concurrent import futures
from threading import Thread
from flask import Flask, request
from flask_restful import Resource, Api

import logging
import grpc
import duplicatedlog_pb2 as my_pb   
import duplicatedlog_pb2_grpc as my_grpc
import time
import uuid

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

messages = {}
masterPort = 50051

class MasterProtocol(my_grpc.ProtocolServicer):
    nodes = {}
    port = masterPort

    def register_secondary_node(self, request, context):
        self.port += 1
        self.nodes[request.message] = self.port
        log.info(f"Registering secondary node on port: {self.port}")
        return my_pb.Response(message=str(self.port))

class MessageApi(Resource):
    def get(self):
        return messages

    def post(self):
        key = str(uuid.uuid4())
        messages[key] = request.form['message']
        replicate(request.form['message'])
        return key

api.add_resource(MessageApi, '/')
protocol = MasterProtocol()

def replicate(msg):
    log.info(f"Sending a message ... {msg}")
    messages[str(uuid.uuid4())] = msg

    for key in protocol.nodes:
        with grpc.insecure_channel("localhost:" + str(protocol.nodes[key])) as channel:
            stub = my_grpc.ProtocolStub(channel)
            response = stub.replicate(my_pb.Request(message=msg))
        log.info(f"Response from {key}: {response.message}")

def test_replication():
    # test message replication
    for count in range(5):
        time.sleep(3)
        replicate("message" + str(count))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc.add_ProtocolServicer_to_server(protocol, server)
    server.add_insecure_port("[::]:" + str(protocol.port))
    server.start()
    log.info(f"Server started, listening on port: {protocol.port}")
    server.wait_for_termination()

def web():
    app.run(debug=True, use_reloader=False, port=masterPort)

if __name__ == "__main__":
    Thread(target=web).start()
    # Thread(target=test_replication).start()
    serve()



