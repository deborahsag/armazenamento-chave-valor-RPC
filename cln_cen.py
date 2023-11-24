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
