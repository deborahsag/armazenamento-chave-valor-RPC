"""
Disciplina: Fundamentos de Sistemas Paralelos e Distribuídos 2023/2 - DCC UFMG
Autora: Deborah Santos Andrade Guimarães (deborah.guimaraes@dcc.ufmg.br)

Segunda parte: cliente do servidor centralizador

########################################################################################################################

Requisições:

mapeamento:
    C,ch - executa o métododo de mapeamento do servidor em busca da chave ch; caso a resposta seja um string vazio, não 
    escreve nada; caso contrário, escreve o string de resposta, seguido de ":" , executa uma RPC do tipo consulta para o
    servidor que foi identificado na resposta do mapeamento e escreve o valor de retorno (que pode ser um string vazio).

término:
    T - dispara a operação de término do servidor, escreve na saída o valor de retorno recebido e termina;
"""
import sys

import grpc

import centralizador_pb2, centralizador_pb2_grpc
import armazenamento_pb2, armazenamento_pb2_grpc


def client_central():
    # Argumento da linha de comando
    id_servico = sys.argv[1]

    # Abrir um canal para o servidor
    channel = grpc.insecure_channel(id_servico)

    # Criar o stub, que vai ser o objeto com referências para os procedimentos remotos (código gerado pelo compilador)
    stub = centralizador_pb2_grpc.CentralizadorChaveValorStub(channel)

    while True:
        try:
            # Entrada padrão
            client_input = input()
            commands = client_input.split(',', maxsplit=2)

            # Consulta
            if commands[0] == 'C':
                # Mapeamento para servidor que possui a chave
                chave = int(commands[1])
                response = stub.mapear(centralizador_pb2.MapRequest(chave=chave))

                if response.id_servico == '':
                    print('')
                    continue

                else:
                    print(f"{response.id_servico}:")

                    # RPC do tipo consulta para o servidor que possui a chave
                    channel_consulta = grpc.insecure_channel(response.id_servico)
                    stub_consulta = armazenamento_pb2_grpc.ArmazenamentoChaveValorStub(channel_consulta)
                    response = stub_consulta.consultar(armazenamento_pb2.QueryRequest(chave=chave))
                    print(response.valor)


            # Término
            elif commands[0] == 'T':
                response = stub.terminar(centralizador_pb2.TerminateRequest())
                print(response.num_chaves)

                # Ao desconectar do servidor o cliente pode fechar o canal.
                channel.close()

            else:
                continue

        except EOFError:
            break


if __name__ == "__main__":
    client_central()
