from concurrent import futures
from threading import Thread
from protocol import Protocol

import logging
import grpc
import duplicatedlog_pb2 as my_pb   
import duplicatedlog_pb2_grpc as my_grpc
import time

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
protocol = Protocol()
       
def send_message(msg):
    log.info("Sending a message ...")
    for key in protocol.nodes:
        with grpc.insecure_channel("localhost:" + str(protocol.nodes[key])) as channel:
            stub = my_grpc.ProtocolStub(channel)
            response = stub.replicate(my_pb.Request(message=msg))
        log.info(f"Response from {key}: {response.message}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc.add_ProtocolServicer_to_server(protocol, server)
    server.add_insecure_port("[::]:" + str(protocol.port))
    server.start()
    log.info(f"Server started, listening on port: {protocol.port}")
    server.wait_for_termination()


if __name__ == "__main__":
    t = Thread(target=serve)
    t.start()
    for count in range(5):
        time.sleep(3)
        send_message("message" + str(count))

    t.join()

    

# TODO: 
# flask add message/ list messages
# store messages in memory
