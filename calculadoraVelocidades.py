import traceback

import logging

import sys

import os

import pandas as pd

import glob

import matplotlib.pyplot as plt

import numpy as np

import time

import math

logging.basicConfig(
    filename=r'relatorioErros.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def capturarExcecao(exctype, value, tb):

    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    print(mensagemErro)

    logging.error(mensagemErro)

if __name__ == "__main__":

    sys.excepthook = capturarExcecao

    try:
        
        diretorioAtual = os.getcwd()

        extensaoArquivo = '*.txt'

        buscaDosTxts = os.path.join(diretorioAtual, extensaoArquivo)

        arrayCaminhosTxt = glob.glob(buscaDosTxts)

        # Vou fazer uma iteração global do algoritmo que é
        # regida pelo número de arquivos txt presentes na pasta.
        numeroDeRepeticoes = len(arrayCaminhosTxt)

        arrayNomesTxt = [os.path.basename(itemDoCaminhosTxt) for itemDoCaminhosTxt in arrayCaminhosTxt]

        # Array para armazenar as arrays de velocidade de subida 
        # de cada arquivo
        arrayDasArraysVelocidadeSubida = []

        # E as de velocidade de descida
        arrayDasArraysVelocidadeDescida = []

        arrayDasArraysVelocidadeSubidaLeitura = []

        arrayDasArraysVelocidadeDescidaLeitura = []

        arrayDasArraysVelocidadeSubidaInstantes = []

        arrayDasArraysVelocidadeDescidaInstantes = []

        arrayDesvioPadraoAmostraVelocidadeSubida = []

        arrayDesvioPadraoAmostraVelocidadeDescida = []

        arrayMediaVelocidadeSubida = []

        arrayMediaVelocidadeDescida = []

        arrayDesvioPadraoAmostraMediaVelocidadeDescida = []

        arrayDesvioPadraoAmostraMediaVelocidadeSubida = []

        pastaResultados = "resultados"

        os.makedirs(pastaResultados, exist_ok=True)

        for i in range(numeroDeRepeticoes):

            time.sleep(0.5)
            print("\nComeçando análise...\n")
            time.sleep(0.5)
            print(f"\nArquivo {arrayNomesTxt[i]}\n")


            arrayDasArraysVelocidadeSubida.append([])

            arrayDasArraysVelocidadeDescida.append([])

            arrayDasArraysVelocidadeSubidaLeitura.append([])

            arrayDasArraysVelocidadeDescidaLeitura.append([])

            arrayDasArraysVelocidadeSubidaInstantes.append([])

            arrayDasArraysVelocidadeDescidaInstantes.append([])

            txtEmAnalise = arrayCaminhosTxt[i]

            # O parâmetro usecols (Não tem mais) garante que as únicas colunas 
            # utilizadas sejam as das strings entregues e o 
            # parâmetro header coloca a segunda linha (linha 1) 
            # como cabeçalho da tabela ignorando a primeira 
            # linha que no nosso contexto nos atrapalha e o 
            # parâmetro sep indica a separação entre os dados, 
            # onde "\t" indica que ela é feita com tab 
            # (Tabulação)
            dataFrameVelocidades = pd.read_csv(txtEmAnalise, sep="\t", header=1, names=['t','vy'])

            # dropna é uma função que exclui linhas onde há dados
            # ausentes (NaN)
            dataFrameVelocidades = dataFrameVelocidades.dropna()

            dataFrameVelocidades.index = range(len(dataFrameVelocidades))

            """print(dataFrameVelocidades.dtypes)  
            print(dataFrameVelocidades.head())"""

            # Retorna o número de linhas
            quantidadeLinhas = dataFrameVelocidades.shape[0]

            for j in range(quantidadeLinhas):

                velocidade = dataFrameVelocidades.iloc[j,1]

                instante = dataFrameVelocidades.iloc[j,0]

                def atribuicaoVelocidadeDescida():

                    arrayDasArraysVelocidadeDescida[i].append(abs(velocidade))

                    arrayDasArraysVelocidadeDescidaLeitura[i].append(velocidade)

                    arrayDasArraysVelocidadeDescidaInstantes[i].append(instante)

                def atribuicaoVelocidadeSubida():

                    arrayDasArraysVelocidadeSubida[i].append(abs(velocidade))

                    arrayDasArraysVelocidadeSubidaLeitura[i].append(velocidade)

                    arrayDasArraysVelocidadeSubidaInstantes[i].append(instante)
                
                def varredor(vel):

                    velocidade = vel

                    ponto = 0

                    if velocidade > 0:

                        ponto += 1

                    elif velocidade < 0:

                        ponto += -1

                    elif velocidade == 0:

                        ponto += 0

                    return ponto
                
                def varrerDianteira():
                    
                    pontuacao = 0

                    indice = dataFrameVelocidades.index[j]

                    diferenca = (quantidadeLinhas-1) - indice

                    if diferenca <= 5:

                        exclusao = 5 - diferenca

                        for k in range(6-exclusao):

                            pontuacao += varredor(dataFrameVelocidades.iloc[(j+k),1])

                    else:

                        for k in range(6):

                            pontuacao += varredor(dataFrameVelocidades.iloc[(j+k),1])

                    return pontuacao


                def varrerTraseira():

                    pontuacao = 0

                    indice = dataFrameVelocidades.index[j]

                    diferenca = 5 - indice

                    if abs(diferenca) <= 5:

                        exclusao = 5 - diferenca

                        for k in range(6-exclusao):

                            pontuacao += varredor(dataFrameVelocidades.iloc[(j-k),1])

                    else:

                        for k in range(6):

                            pontuacao += varredor(dataFrameVelocidades.iloc[(j-k),1])

                    return pontuacao

                # Primeiro, vamos descobrir se o ponto analisado 
                # vai estar em um dos extremos ou no meio

                if velocidade == 0:
                    
                    Pontuacao = varrerDianteira()

                    if Pontuacao > 0:

                        atribuicaoVelocidadeSubida()

                    elif Pontuacao < 0:

                        atribuicaoVelocidadeDescida()


                elif velocidade != 0 and velocidade != (quantidadeLinhas-1):

                    PontuacaO = varrerDianteira() + varrerTraseira()

                    if PontuacaO > 0:

                        atribuicaoVelocidadeSubida()

                    elif PontuacaO < 0:

                        atribuicaoVelocidadeDescida()

                    elif PontuacaO == 0:

                        if varrerTraseira() < 0:

                            atribuicaoVelocidadeDescida()

                        elif varrerTraseira() > 0:

                            atribuicaoVelocidadeSubida()


                elif velocidade == (quantidadeLinhas-1):

                    pontuacaO = varrerTraseira()

                    if pontuacaO > 0:

                        atribuicaoVelocidadeSubida()

                    elif pontuacaO < 0:

                        atribuicaoVelocidadeDescida()

            print(f"\nGerando gráfico para {arrayNomesTxt[i]}\n")

            plt.plot(arrayDasArraysVelocidadeSubidaInstantes, arrayDasArraysVelocidadeSubidaLeitura, color="red", marker='.')

            plt.plot(arrayDasArraysVelocidadeDescidaInstantes, arrayDasArraysVelocidadeDescidaLeitura, color="blue", marker='.')

            plt.plot(dataFrameVelocidades['t'], dataFrameVelocidades['vy'], color='black', linestyle='--')

            plt.title('Velocidade de subida em vermelho e velocidade de descida em azul')
            plt.xlabel('Instante (s)')
            plt.ylabel('Velocidade vertical (m/s)')
            plt.gcf().canvas.manager.set_window_title(f"Velocidade em função do tempo para {arrayNomesTxt[i]}")

            print("\nATENÇÃO, feche a janela do gráfico para prosseguir\n")

            plt.show()

            desvioPadraoAmostralVelocidadeDescida = np.std(arrayDasArraysVelocidadeDescida[i], ddof=1)

            desvioPadraoAmostralVelocidadeSubida = np.std(arrayDasArraysVelocidadeSubida[i], ddof=1)

            arrayDesvioPadraoAmostraVelocidadeSubida.append(desvioPadraoAmostralVelocidadeSubida)

            arrayDesvioPadraoAmostraVelocidadeDescida.append(desvioPadraoAmostralVelocidadeDescida)

            arrayMediaVelocidadeSubida.append(np.mean(arrayDasArraysVelocidadeSubida[i]))

            arrayMediaVelocidadeDescida.append(np.mean(arrayDasArraysVelocidadeDescida[i]))

            arrayDesvioPadraoAmostraMediaVelocidadeDescida.append(desvioPadraoAmostralVelocidadeDescida/(math.sqrt(len(arrayDasArraysVelocidadeDescida[i]))))

            arrayDesvioPadraoAmostraMediaVelocidadeSubida.append(desvioPadraoAmostralVelocidadeSubida/(math.sqrt(len(arrayDasArraysVelocidadeSubida[i]))))

            subpastaArquivos = f"{arrayNomesTxt[i]}"

            caminho = os.path.join(pastaResultados,subpastaArquivos)

            os.makedirs(f"{pastaResultados}/{subpastaArquivos}", exist_ok=True)

            caminho = os.path.join(pastaResultados,subpastaArquivos)

            caminho_arquivo_resultadosVelSub = os.path.join(caminho, f"velSub.csv")

            caminho_arquivo_resultadosVelDes = os.path.join(caminho, f"velDes.csv")

            csv_VelSub = []

            csv_VelDes = []

            for velocidadeSubida in arrayDasArraysVelocidadeSubidaLeitura[i]:

                csv_VelSub.append(velocidadeSubida)

            dfVelSub = pd.DataFrame(csv_VelSub, columns=["Velocidade de subida"])

            dfVelSub.to_csv(caminho_arquivo_resultadosVelSub, sep="\t", index=True)

            for velocidadeDescida in arrayDasArraysVelocidadeDescidaLeitura[i]:

                csv_VelDes.append(velocidadeDescida)

            dfVelDes = pd.DataFrame(csv_VelDes, columns=[ "Velocidade de descida"])

            dfVelDes.to_csv(caminho_arquivo_resultadosVelDes, sep="\t", index=True)

            print(f"\nVelocidades de cada grupo salvas para o arquivo {arrayNomesTxt[i]} em {caminho}\n")

            print(f"\nÁnalise do arquivo {arrayNomesTxt[i]} finalizada\n")

        estatisticas = {
            "nome": arrayNomesTxt,
            "mediaVelSub": arrayMediaVelocidadeSubida,
            "desvPadVelSub": arrayDesvioPadraoAmostraVelocidadeSubida,
            "media_DesvPadVelSub_Erro": arrayDesvioPadraoAmostraMediaVelocidadeSubida,
            "mediaVelDes": arrayMediaVelocidadeDescida,
            "desvPadVelDes": arrayDesvioPadraoAmostraVelocidadeDescida,
            "media_DesvPadVelDes_Erro": arrayDesvioPadraoAmostraMediaVelocidadeDescida
        }

        dataFrameEstatisticas = pd.DataFrame(estatisticas)

        caminho_arquivo_estatisticas = os.path.join(pastaResultados, "estatisticas.csv")

        dataFrameEstatisticas.to_csv(caminho_arquivo_estatisticas, sep="\t", index=True)

        print(f"\nEstatísticas de todos os grupos reunidas em {caminho_arquivo_estatisticas}\n")

    except Exception as e:

        capturarExcecao(*sys.exc_info())
        input("Pressione Enter para sair...")

