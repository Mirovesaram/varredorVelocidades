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
        
        diretorio_atual = os.getcwd()

        arquivo = 'gotas.xlsx'

        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} não encontrado no diretório atual.")
        else:
            dataframeCargasGota = pd.read_excel(arquivo)
            #print(dataframeCargasGota)

        #print(dataframeCargasGota['Carga'].dtype)

        arrayCargaElementarVariavel = []

        for i in np.arange(1.6 * 10**(-19), 1.91 * 10**(-19), 0.01 * 10**(-19)):
            arrayCargaElementarVariavel.append(format(i, ".2e"))
        
        quantidadeItens = len(arrayCargaElementarVariavel)

        for i in range(quantidadeItens):
            arrayCargaElementarVariavel[i] = float(arrayCargaElementarVariavel[i])

        #print(quantidadeItens)
        #print(type(arrayCargaElementarVariavel))
        #arrayCargaElementarVariavel = arrayCargaElementarVariavel*10**(-19)
        #print(arrayCargaElementarVariavel)

        arrayConjuntosInteiros = []



        for i in range(quantidadeItens):
            cargaElementarAtual = arrayCargaElementarVariavel[i]
            #print(type(cargaElementarAtual))
            conjuntoInteiros = (dataframeCargasGota['Carga']/cargaElementarAtual)
            conjuntoInteiros = round(conjuntoInteiros)
            #print(len(conjuntoInteiros))
            arrayConjuntosInteiros.append(conjuntoInteiros)
            #print(conjuntoInteiros)

        

        #print(len(arrayConjuntosInteiros))
        quantidadeGotas = len(dataframeCargasGota.iloc[:,0])

        for i in range(quantidadeItens):
            for j in range(quantidadeGotas):
                if arrayConjuntosInteiros[i][j] == 0:
                    arrayConjuntosInteiros[i][j] += 1
        #print(quantidadeGotas)
        arrayValoresCargaElementar = []

        for i in range(quantidadeItens):
            arrayValoresCargaElementar.append([])

        for i in range(quantidadeItens):
            for j in range(quantidadeGotas):
                valorCargaElementar = (dataframeCargasGota.iloc[j,0])/(arrayConjuntosInteiros[i][j])
                arrayValoresCargaElementar[i][j].append(valorCargaElementar)
            print(arrayCargaElementarVariavel[i])

        
        
        """for i in range(quantidadeItens):
            print(arrayConjuntosInteiros)"""
            
        
        

        #print(valoresCargaElementar)
            
        
    #Exceto se
    except Exception as e:
        #Utiliza o método global para mostrar o erro no código
        capturarExcecao(*sys.exc_info())