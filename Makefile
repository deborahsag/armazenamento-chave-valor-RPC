all:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. armazenamento.proto

clean:
	rm -rf armazenamento_pb2.py armazenamento_pb2_grpc.py