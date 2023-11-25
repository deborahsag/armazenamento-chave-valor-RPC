"""
Disciplina: Fundamentos de Sistemas Paralelos e Distribuídos 2023/2 - DCC UFMG
Autora: Deborah Santos Andrade Guimarães (deborah.guimaraes@dcc.ufmg.br)

Primeira parte: cliente do servidor de pares (chave, valor)

########################################################################################################################

Requisições (entrada padrão):

inserção:
    I,ch, string de descrição - insere no servidor a chave ch, associada ao string de descrição como seu valor, escreve
    na saída padrão o valor de retorno do procedimento (0 ou -1);

consulta:
    C,ch - consulta o servidor pelo conteúdo associado à chave ch e escreve na saída o string definido como valor, que
    pode ser nulo, caso a chave não seja encontrada;

ativação:
    A,string identificador de um serviço - aciona o método de ativação do servidor passando o string identificador como
    parâmetro e escrevendo na saída o valor inteiro devolvido pelo servidor;

término:
    T - termina a operação do servidor, que envia zero como valor de retorno e termina (somente nesse caso o cliente
    deve terminar a execução do servidor; se a entrada terminar sem um comando T, o cliente deve terminar sem acionar o
    término do servidor).
"""
from __future__ import print_function

import sys

import grpc

import armazenamento_pb2, armazenamento_pb2_grpc


def client_par():
    # Argumento da linha de comando
    id_servico  = sys.argv[1]

    # Abrir um canal para o servidor
    channel = grpc.insecure_channel(id_servico)

    # Criar o stub, que vai ser o objeto com referências para os procedimentos remotos (código gerado pelo compilador)
    stub = armazenamento_pb2_grpc.ArmazenamentoChaveValorStub(channel)

    while True:
        try:
            # Entrada padrão
            client_input = input()
            commands = client_input.split(',', maxsplit=2)

            # Inserção
            if commands[0] == 'I':
                chave = int(commands[1])
                valor = commands[2]
                response = stub.inserir(armazenamento_pb2.InsertRequest(chave=chave, valor=valor))
                print(response.retorno)

            # Consulta
            elif commands[0] == 'C':
                chave = int(commands[1])
                response = stub.consultar(armazenamento_pb2.QueryRequest(chave=chave))
                print(response.valor)

            # Ativação
            elif commands[0] == 'A':
                id_servico = commands[1]
                response = stub.ativar(armazenamento_pb2.ActivateRequest(id_servico=id_servico))
                print(response.retorno)

            # Término
            elif commands[0] == 'T':
                response = stub.terminar(armazenamento_pb2.TerminateRequest())
                print(response.retorno)

                # Ao desconectar do servidor o cliente pode fechar o canal.
                channel.close()

            else:
                continue

        except EOFError:
            break


if __name__ == '__main__':
    client_par()
