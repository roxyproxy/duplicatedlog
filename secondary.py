from concurrent import futures
from threading import Thread
from flask import Flask
from flask_restful import Resource, Api

import logging
import uuid
import grpc
import duplicatedlog_pb2 as my_pb
import duplicatedlog_pb2_grpc as my_grpc
import os
import time

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

class SecondaryProtocol(my_grpc.ProtocolServicer):
    def replicate(self, request, context):
        time.sleep(int(os.getenv('DELAY')))
        log.info(f"Received: {request.message}")
        messages[str(uuid.uuid4())] = request.message
        return my_pb.Response(message="ok")

class MessageApi(Resource):
    def get(self):
        return messages

api.add_resource(MessageApi, '/')
protocol = SecondaryProtocol()
messages = {} 

def add_node():
    with grpc.insecure_channel(os.getenv('MASTER_GRPC_HOST') + ":" + os.getenv('MASTER_GRPC_PORT')) as channel:
        stub = my_grpc.ProtocolStub(channel)
        response = stub.register_secondary_node(my_pb.Request(message=str(os.getenv('SECONDARY_GRPC_HOST') + ":" + os.getenv('SECONDARY_GRPC_PORT'))))
    log.info(f"Registered secondary node: {os.getenv('SECONDARY_GRPC_HOST')}:{os.getenv('SECONDARY_GRPC_PORT')}")
    return response.message

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc.add_ProtocolServicer_to_server(protocol, server)
    server.add_insecure_port(os.getenv('SECONDARY_GRPC_HOST') + ":" + os.getenv('SECONDARY_GRPC_PORT'))
    server.start()
    log.info(f"Secondary node started: {os.getenv('SECONDARY_GRPC_HOST')}:{os.getenv('SECONDARY_GRPC_PORT')}")
    server.wait_for_termination()

def web():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=os.getenv('SECONDARY_PORT'))

if __name__ == "__main__":
    nodeid = add_node()
    Thread(target=web).start()
    serve()