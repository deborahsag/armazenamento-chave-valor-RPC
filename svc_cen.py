"""
Disciplina: Fundamentos de Sistemas Paralelos e Distribuídos 2023/2 - DCC UFMG
Autora: Deborah Santos Andrade Guimarães (deborah.guimaraes@dcc.ufmg.br)

Segunda parte: servidor centralizador

########################################################################################################################

Procedimentos fornecidos:

diretorio:
    recebe como parâmetro o string identificador de serviço que identifica um servidor de armazenamento de pares 
    chave/valor e a lista de chaves (inteiros) nele armazenadas, armazena cada chave em seu diretório, associando-as ao 
    identificador de serviço recebido, e retorna o número de chaves que foram processadas;
    
mapeamento: 
    recebe como parâmetro um inteiro positivo ch, consulta o seu diretório de chaves por servidor e retorna o string 
    identificador de serviço associado ao servidor que contém um par com aquela chave, ou um string vazio, caso não 
    encontre tal servidor;
    
término: 
    encerra a operação do servidor centralizador apenas, retorna o número de chaves que estavam registradas e termina. 
"""
import sys

from concurrent import futures  # usado na definição do pool de threads
import threading

import grpc

import centralizador_pb2, centralizador_pb2_grpc


class CentralizadorChaveValor(centralizador_pb2_grpc.CentralizadorChaveValorServicer):
    def __init__(self, stop_event, porto):
        self._stop_event = stop_event
        self.diretorio = {}
        self.porto = porto

    def registrar(self, request, context):
        for ch in request.chaves:
            self.diretorio[ch] = request.id_servico
        num_chaves = len(request.chaves)
        return centralizador_pb2.RegisterResponse(num_chaves=num_chaves)

    def mapear(self, request, context):
        chave = int(request.chave)
        if chave in self.diretorio:
            id_servico = self.diretorio[chave]
            return centralizador_pb2.MapResponse(id_servico=id_servico)
        else:
            return centralizador_pb2.MapResponse(id_servico='')

    def terminar(self, request, context):
        self._stop_event.set()
        num_chaves = len(self.diretorio.keys())
        return centralizador_pb2.TerminateResponse(num_chaves=num_chaves)


def server_central():
    # Argumentos da linha de comando
    porto = sys.argv[1]

    # Evento para terminar o servidor remotamente
    stop_event = threading.Event()

    # O servidor usa um modelo de pool de threads do pacote concurrent
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # O servidor precisa ser ligado ao objeto que identifica os
    #   procedimentos a serem executados.
    centralizador_pb2_grpc.add_CentralizadorChaveValorServicer_to_server(
        CentralizadorChaveValor(stop_event, porto), server
    )

    # O método add_insecure_port permite a conexão direta por TCP
    server.add_insecure_port(f'0.0.0.0:{porto}')

    # O servidor é iniciado e termina quando o evento stop eh acionado
    server.start()
    stop_event.wait()
    server.stop(0)


if __name__ == "__main__":
    server_central()
