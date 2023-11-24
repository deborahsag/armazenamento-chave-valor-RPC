"""
Disciplina: Fundamentos de Sistemas Paralelos e Distribuídos 2023/2 - DCC UFMG
Autora: Deborah Santos Andrade Guimarães (deborah.guimaraes@dcc.ufmg.br)

Segunda parte: servidor centralizador

########################################################################################################################

Procedimentos fornecidos:

registro: 
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
