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

        # Elemento desnecessário agora
        """voltagem = int(input("Insira a voltagem da pasta\n"))

        if (voltagem <= 0) or (voltagem % 50 != 0):
            print("Insira um valor válido.")
            sys.exit()"""

        caminho_raiz = os.getcwd()

        # Setado para pegar todo arquivo .csv
        lista_csv = glob.glob(f"{caminho_raiz}/**/*.csv", recursive=True)

        print(lista_csv)

        print(len(lista_csv))

        dataframes = [pd.read_csv(arquivo, sep=",", decimal=",", index_col=False) for arquivo in lista_csv]

        dataframeVelocidades = pd.concat(dataframes, ignore_index=True)

        # Não necessário agora
        """dataframeVelocidades["Voltagem"] = voltagem"""

        caminhoResultado = os.path.join(caminho_raiz, f"velocidades.csv")

        dataframeVelocidades.to_csv(caminhoResultado, index=True)

    except Exception as e:

        capturarExcecao(*sys.exc_info())
        input("Pressione Enter para sair...")