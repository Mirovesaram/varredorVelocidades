import logging

import os

import sys

import traceback

import pandas as pd

import matplotlib

import numpy as np

#Método para capturar erros de forma global
def capturarExcecao(exctype,value,tb):

    #Essa é a mensagem de erro com detalhes de onde o erro aconteceu no código
    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    print(mensagemErro)

    #Esse é o comando para inserir o erro no arquivo .log
    logging.error(mensagemErro)

    
if __name__ == "__main__":
    #O erro do sistema vai ser direcionado ao método global (Acho)
    sys.excepthook=capturarExcecao
    #Tente
    try:
        
        # MÉTODOS DE ATRIBUIÇÃO

        # MÉTODOS DE EXECUÇÃO

        # MÉTODOS DE EDIÇÃO

        # MÉTODOS DE AVALIAÇÃO

        pass
        
    #Exceto se
    except Exception as e:
        #Utiliza o método global para mostrar o erro no código
        capturarExcecao(*sys.exc_info())