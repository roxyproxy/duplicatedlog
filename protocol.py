import logging
import duplicatedlog_pb2 as my_pb
import duplicatedlog_pb2_grpc as my_grpc

logging.basicConfig(format='%(asctime)s: : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

class Protocol(my_grpc.ProtocolServicer):
    masterPort = 50051
    nodes = {}
    port = masterPort

    def register_secondary_node(self, request, context):
        self.port += 1
        self.nodes[request.message] = self.port
        log.info(f"Registering secondary node on port: {self.port}")
        return my_pb.Response(message=str(self.port))
    
    def replicate(self, request, context):
        log.info(f"Received: {request.message}")
        return my_pb.Response(message="ok")