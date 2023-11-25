"""
Disciplina: Fundamentos de Sistemas Paralelos e Distribuídos 2023/2 - DCC UFMG
Autora: Deborah Santos Andrade Guimarães (deborah.guimaraes@dcc.ufmg.br)

Primeira parte: servidor de pares (chave, valor)

########################################################################################################################

Procedimentos fornecidos:

inserção:
    recebe como parâmetros um inteiro positivo (chave) e um string, e armazena o string em um dicionário, associado à
    chave, caso ela ainda não exista, retornando zero; caso a chave já exista o conteúdo não deve ser alterado e o valor
     -1 deve ser retornado;

consulta:
    recebe como parâmetros um inteiro positivo (chave) e retorna o conteúdo do string associado à chave, caso ela
    exista, ou um string nulo caso contrário;

ativação:
    recebe como parâmetro um string identificador de um serviço e uma flag opcional que determina se um servidor
    centralizador será utilizado ou não;

término:
    um procedimento sem parâmetros que indica que o servidor deve terminar sua execução; nesse caso o servidor deve
    responder com zero e terminar sua execução depois da resposta . O cliente deve escrever na saída o valor de retorno
    do servidor e terminar em seguida.
"""
import sys

from concurrent import futures  # usado na definição do pool de threads
import threading
import socket

import grpc

import armazenamento_pb2, armazenamento_pb2_grpc    # módulos gerados pelo compilador de gRPC
import centralizador_pb2, centralizador_pb2_grpc


class ArmazenamentoChaveValor(armazenamento_pb2_grpc.ArmazenamentoChaveValorServicer):
    def __init__(self, stop_event, porto, flag_ativacao):
        self._stop_event = stop_event
        self.armazem = {}
        self.porto = porto
        self.flag_ativacao = flag_ativacao
        self.stub_central = None

    def inserir(self, request, context):
        chave = request.chave
        valor = request.valor
        if chave in self.armazem:
            return armazenamento_pb2.InsertResponse(retorno=-1)
        else:
            self.armazem[chave] = valor
        return armazenamento_pb2.InsertResponse(retorno=0)

    def consultar(self, request, context):
        chave = request.chave
        if chave in self.armazem:
            return armazenamento_pb2.QueryResponse(valor=self.armazem[chave])
        else:
            return armazenamento_pb2.QueryResponse(valor='')

    def ativar(self, request, context):
        if self.flag_ativacao:
            # Entrada: id_servico do servidor centralizador
            id_servico_central = request.id_servico

            # Faz a conexao com o servidor centralizador
            channel_central = grpc.insecure_channel(id_servico_central)
            self.stub_central = centralizador_pb2_grpc.CentralizadorChaveValorStub(channel_central)

            # Registra o proprio id e as chaves que possui
            self_id_servico_nome = socket.getfqdn()
            self_id_servico = f"{self_id_servico_nome}:{self.porto}"
            chaves = list(self.armazem.keys())
            response = self.stub_central.registrar(
                centralizador_pb2.RegisterRequest(id_servico=self_id_servico, chaves=chaves))

            return armazenamento_pb2.ActivateResponse(retorno=len(chaves))

        else:
            return armazenamento_pb2.ActivateResponse(retorno=0)

    def terminar(self, request, context):
        self._stop_event.set()
        return armazenamento_pb2.TerminateResponse(retorno=0)


def server_par():
    # Argumentos da linha de comando
    porto = sys.argv[1]
    if len(sys.argv) > 2:
        flag_ativacao = True
    else:
        flag_ativacao = False

    # Evento para terminar o servidor remotamente
    stop_event = threading.Event()

    # O servidor usa um modelo de pool de threads do pacote concurrent
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # O servidor precisa ser ligado ao objeto que identifica os
    #   procedimentos a serem executados.
    armazenamento_pb2_grpc.add_ArmazenamentoChaveValorServicer_to_server(
        ArmazenamentoChaveValor(stop_event, porto, flag_ativacao), server
    )

    # O método add_insecure_port permite a conexão direta por TCP
    server.add_insecure_port(f'0.0.0.0:{porto}')

    # O servidor é iniciado e termina quando o evento stop eh acionado
    server.start()
    stop_event.wait()
    server.stop(0)


if __name__ == '__main__':
    server_par()
