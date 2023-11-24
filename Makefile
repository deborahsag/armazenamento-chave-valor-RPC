all:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. armazenamento.proto

run_serv_pares_1:
	python3 svc_par.py $(arg)
run_serv_pares_2:
	python3 svc_par.py $(arg) ativacao  # como descrito, o segundo argumento só tem que existir
run_cli_pares:
	python3 cln_par.py $(arg)
run_serv_central:
	python3 svc_cen.py $(arg)
run_cli_central:
	python3 cln_cen.py $(arg)

clean:
	rm -rf armazenamento_pb2.py armazenamento_pb2_grpc.py
