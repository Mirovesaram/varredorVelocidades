import logging

import os

import sys

import traceback

import pandas as pd

import matplotlib

import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from interfaceGerada.janelaAtribuicao import Ui_janelaAtribuicao

# Tentar resolver problema dos ícones que não estão aparecendo nas janelas, solução
# retirada de:
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(caminho_relativo):
    try:
        caminho_base = sys._MEIPASS

    except Exception:

        caminho_base = os.path.abspath(".")

    return os.path.join(caminho_base, caminho_relativo)

#Método para capturar erros de forma global
def capturarExcecao(exctype,value,tb):

    #Essa é a mensagem de erro com detalhes de onde o erro aconteceu no código
    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    print(mensagemErro)

    #Esse é o comando para inserir o erro no arquivo .log
    logging.error(mensagemErro)

class MainWindow(QMainWindow, Ui_janelaAtribuicao):
            
            def __init__(self):

                super().__init__()

                self.setupUi(self)

                self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

            
            def buscarDirArquivosTxt(self):
                
                diretorio=None      
                
                opcoes = QFileDialog.Options()
                
                opcoes |= QFileDialog.ShowDirsOnly
                
                diretorio = QFileDialog.getExistingDirectory(self,'Selecionar Pasta dos CIFs','',options=opcoes)
                
                if diretorio:
                    
                    self.textEditCaminhoPasta.setText(diretorio)

                    return diretorio
                
                else:

                    self.textEditCaminhoPasta.setText('O caminho aparecerá aqui quando selecionado')
            

        
        # MÉTODOS DE ATRIBUIÇÃO

        # MÉTODOS DE EXECUÇÃO

        # MÉTODOS DE EDIÇÃO

        # MÉTODOS DE AVALIAÇÃO


    
if __name__ == "__main__":
    #O erro do sistema vai ser direcionado ao método global (Acho)
    sys.excepthook=capturarExcecao
    #Tente
    try:

        app = QApplication(sys.argv)

        window = MainWindow()

        window.show()

        sys.exit(app.exec_())
        
    #Exceto se
    except Exception as e:


        #Utiliza o método global para mostrar o erro no código
        capturarExcecao(*sys.exc_info())