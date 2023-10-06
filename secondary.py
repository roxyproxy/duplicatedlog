from concurrent import futures
from protocol import Protocol

import logging
import uuid
import grpc
import duplicatedlog_pb2 as my_pb
import duplicatedlog_pb2_grpc as my_grpc

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
protocol = Protocol()
nodeid = uuid.uuid4()

def add_node():
    log.info("Registering secondary node ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = my_grpc.ProtocolStub(channel)
        response = stub.register_secondary_node(my_pb.Request(message=str(nodeid)))
    log.info(f"Registered on port: {response.message}")
    return response.message

def serve():
    port = add_node()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc.add_ProtocolServicer_to_server(protocol, server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    log.info(f"Server started, listening on port: {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
