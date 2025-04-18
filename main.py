import logging

import os

import sys

import traceback

import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

import glob

import time

import math

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from PyQt5.QtCore import QDir

from PyQt5.QtGui import QIcon

from interfaceGerada.janelaAtribuicao import Ui_janelaAtribuicao

from interfaceGerada.janelaExecucao import Ui_MainWindowExecucao

# Tentar resolver problema dos ícones que não estão aparecendo nas janelas, solução
# retirada de:
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(caminho_relativo):
    try:
        caminho_base = sys._MEIPASS

    except Exception:

        caminho_base = os.path.abspath(".")

    return os.path.join(caminho_base, caminho_relativo)

# Configuração básica para criação do arquivo.log

logging.basicConfig(
    filename=r'relatorioErros.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Método para capturar erros de forma global
def capturarExcecao(exctype,value,tb):

    # Essa é a mensagem de erro com detalhes de 
    # onde o erro aconteceu no código
    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    # Esse é o comando para inserir o erro no arquivo .log
    logging.error(mensagemErro)

    # Cria-se uma caixa de erro
    erro=QMessageBox()
    # Coloca-se o ícone da caixa como crítico
    erro.setIcon(QMessageBox.Critical)
    # Insere o texto na caixa de erro
    erro.setText("Ocorreu um erro no aplicativo")
    # E também insere o erro que aconteceu
    erro.setInformativeText(str(value))
    # Esse é o título que aparecerá na caixa,
    # No canto superior esquerdo da caixa
    erro.setWindowTitle("Erro")
    # Comando para adicionar um ícone ao canto superior
    # esquerdo da janela
    erro.setWindowIcon(QIcon(resource_path(r'icones\logoMillikan.ico')))
    # E os detalhes do erro, como onde
    # ocorreu nas linhas de código
    erro.setDetailedText(mensagemErro)
    # Comando para quando fechar a caixa, encerrar o programa
    erro.exec_()

class MainWindow(QMainWindow, Ui_janelaAtribuicao):
            
    def __init__(self):

        super().__init__()

        self.setupUi(self)

        self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        self.janela_atribuicao = QMainWindow()

        self.janelaAtribuicao = Ui_janelaAtribuicao()

        self.janelaAtribuicao.setupUi(self.janela_atribuicao)

        self.janela_execucao = QMainWindow()

        self.janelaExecucao = Ui_MainWindowExecucao()

        self.janelaExecucao.setupUi(self.janela_execucao)

        self.progressBar = self.janelaExecucao.progressBarExecucao

        self.janelaExecucao.pushButtonCancelar.clicked.connect(self.cancelarOsCalculosFeitos)

        ############
        ############
        # GATILHOS #
        ############
        ############

        self.pushButtonSelecPasta.clicked.connect(self.buscarDirArquivosTxt)

        self.pushButton_executar.clicked.connect(self.extrairVariaveis)

        #############
        #############
        # ATRIBUTOS #
        #############
        #############

        # Array das arrays de velocidades de subida e descida
        self.arrayDasArraysVelSub = []

        self.arrayDasArraysVelDes = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades de subida e descida
        self.arrayDasArraysVelSubInstantes = []

        self.arrayDasArraysVelDesInstantes = []

        # Array de desvios padrões amostrais das velocidades 
        # de subida e descida
        self.arrayDesvPadAmostVelSub = []

        self.arrayDesvPadAmostVelDes = []

        #Array de médias das velocidades de subida e descida
        self.arrayMediaVelSub = []

        self.arrayMediaVelDes = []

        # Array de desvios padrões amostrais da média de (erros) 
        # velocidades de subida e descida
        self.arrayDesvPadAmostMediaVelDes = []

        self.arrayDesvPadAmostMediaVelSub = []

        # Array dos caminhos dos arquivos .txt
        self.arrayCaminhosArquivos = None

        # Inicialização do atributo diretório
        self.diretorio = None
        
        # Inicialização do atributo voltagem
        self.voltagem = None

        # Inicialização do atributo densidade da gota
        self.densGot = None

        # Inicialização do atributo distância das placas
        self.distPlacs = None

        # Inicialização do atributo varredura
        self.varredura = 5

    #########################
    #########################            
    # MÉTODOS DE ATRIBUIÇÃO #
    #########################
    #########################

    # Método para exibir diretórios e conseguir o caminho da pasta
    
    def buscarDirArquivosTxt(self):

        self.diretorio = None
        
        diretorio=None      
        
        opcoes = QFileDialog.Options()
        
        opcoes |= QFileDialog.ShowDirsOnly
        
        diretorio = QFileDialog.getExistingDirectory(self,'Selecionar Pasta','',options=opcoes)
        
        if diretorio:
            
            self.textEditCaminhoPasta.setText(diretorio)

            self.diretorio = diretorio

            # Para fins de teste

            #print(self.diretorio)
        
        else:

            self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")
            
            # Para fins de teste

            #print(self.diretorio)

    # Método para verificar se tudo foi devidamente 
    # preenchido e então extrair as variáveis para
    # executar os cálculos

    def extrairVariaveis(self):
            
        densGot = self.doubleSpinBoxDensGot.value()

        distPlacs = self.doubleSpinBox_distPlacs.value()

        voltagem = self.doubleSpinBox_voltagem.value()
        
        if densGot != 0 and voltagem != 0 and distPlacs != 0:
        
            if self.diretorio:

                self.voltagem = voltagem

                self.densGot = densGot

                self.distPlacs = distPlacs

                # Para fins de teste

                #print(f"{voltagem}, {distPlacs}, {densGot}")

                arrayCaminhosTxt = []

                extensaoArquivo = '*.txt'

                buscaDosTxts = os.path.join(self.diretorio, extensaoArquivo)

                arrayCaminhosTxt = glob.glob(buscaDosTxts)

                if arrayCaminhosTxt != []:

                    self.executarCalculos(arrayCaminhosTxt)

                else:
                    
                    QMessageBox.warning(self, "Erro", "A pasta que você escolheu não tem nenhum arquivo .txt")

            else:

                QMessageBox.warning(self, "Erro", "Você não escolheu uma pasta.")
        
        else:
            
            QMessageBox.warning(self, "Erro", "Preencha os campos corretamente. Algum deles está nulo.")

        #######################
        #######################
        # MÉTODOS DE EXECUÇÃO #
        #######################
        #######################

    def atualizar_progresso(self, valor, mensagem):

        self.progressBar.setValue(valor)
        self.progressBar.setFormat(f"{mensagem} ({valor}%)")
        QApplication.processEvents()

    def executarCalculos(self, arrayCaminhosTxt):

        self.hide()

        self.janela_execucao.show()

        self.close()
        
        time.sleep(0.5)
        self.atualizar_progresso(0, "Iniciando processamento")
        time.sleep(0.5)

        # Vou fazer uma iteração global do algoritmo que é
        # regida pelo número de arquivos txt presentes na pasta.
        numeroDeRepeticoes = len(arrayCaminhosTxt)

        # splitext é para excluir a extensão .txt do fim do nome base (basename)
        arrayNomesTxt = [os.path.splitext(os.path.basename(itemDoCaminhosTxt))[0] for itemDoCaminhosTxt in arrayCaminhosTxt]

        pastaResultados = "resultados"

        os.makedirs(pastaResultados, exist_ok=True)

        time.sleep(0.5)
        self.atualizar_progresso(10, "Iniciando Varredura")
        time.sleep(0.5)

        self.varredura = 5

        for i in range(numeroDeRepeticoes):

            time.sleep(0.5)
            self.atualizar_progresso((20+(i+1)), "Varrendo...")
            time.sleep(0.5)

            #time.sleep(0.5)
            #print("\nComeçando análise...\n")
            #time.sleep(0.5)
            #print(f"\nArquivo {arrayNomesTxt[i]}\n")

            self.arrayDasArraysVelSub.append([])

            self.arrayDasArraysVelDes.append([])

            self.arrayDasArraysVelSubInstantes.append([])

            self.arrayDasArraysVelDesInstantes.append([])

            txtEmAnalise = arrayCaminhosTxt[i]

            # O parâmetro usecols (Não tem mais) garante que as únicas colunas 
            # utilizadas sejam as das strings entregues e o 
            # parâmetro header coloca a segunda linha (linha 1) 
            # como cabeçalho da tabela ignorando a primeira 
            # linha que no nosso contexto nos atrapalha e o 
            # parâmetro sep indica a separação entre os dados, 
            # onde "\t" indica que ela é feita com tab 
            # (Tabulação)

            try:
                
                dataFrameVelocidades = pd.read_csv(txtEmAnalise, sep="\t", header=1, names=['t','vy'])

            except Exception as e:
                 
                 self.cancelarOsCalculosFeitos()

                 raise ValueError(f"O dataframe do arquivo {txtEmAnalise} apresenta problemas")

            # dropna é uma função que exclui linhas onde há dados
            # ausentes (NaN)
            dataFrameVelocidades = dataFrameVelocidades.dropna()

            #dataFrameVelocidades.index = range(len(dataFrameVelocidades))

            #print(dataFrameVelocidades.dtypes)  
            #print(dataFrameVelocidades.head())

            self.classificarVelocidades(dataFrameVelocidades, i)

            #print(f"\nGerando gráfico para {arrayNomesTxt[i]}\n")

            """plt.scatter(self.arrayDasArraysVelSubInstantes[i], self.arrayDasArraysVelSub[i], color="red", marker='.')

            plt.scatter(self.arrayDasArraysVelDesInstantes[i], self.arrayDasArraysVelDes[i], color="blue", marker='.')

            plt.plot(dataFrameVelocidades['t'], dataFrameVelocidades['vy'], color='black', linestyle='--')

            plt.title('Velocidade de subida em vermelho e velocidade de descida em azul')
            plt.xlabel('Instante (s)')
            plt.ylabel('Velocidade vertical (m/s)')
            plt.gcf().canvas.manager.set_window_title(f"Velocidade em função do tempo para {arrayNomesTxt[i]}")

            #print("\nATENÇÃO, feche a janela do gráfico para prosseguir\n")

            plt.savefig(os.path.join(pastaResultados, f"grafico{arrayNomesTxt[i]}_var{self.varredura}.png"), dpi=300, bbox_inches='tight')

            plt.show()"""

            desvioPadraoAmostralVelocidadeDescida = np.std(self.arrayDasArraysVelDes[i], ddof=1)

            desvioPadraoAmostralVelocidadeSubida = np.std(self.arrayDasArraysVelSub[i], ddof=1)

            self.arrayDesvPadAmostVelSub.append(desvioPadraoAmostralVelocidadeSubida)

            self.arrayDesvPadAmostVelDes.append(desvioPadraoAmostralVelocidadeDescida)

            self.arrayMediaVelSub.append(np.mean(self.arrayDasArraysVelSub[i]))

            self.arrayMediaVelDes.append(np.mean(self.arrayDasArraysVelDes[i]))

            self.arrayDesvPadAmostMediaVelDes.append(desvioPadraoAmostralVelocidadeDescida/(math.sqrt(len(self.arrayDasArraysVelDes[i]))))

            self.arrayDesvPadAmostMediaVelSub.append(desvioPadraoAmostralVelocidadeSubida/(math.sqrt(len(self.arrayDasArraysVelSub[i]))))

            #subpastaArquivos = f"{arrayNomesTxt[i]}"

            #caminho = os.path.join(pastaResultados,subpastaArquivos)

            #os.makedirs(f"{pastaResultados}/{subpastaArquivos}", exist_ok=True)

            #caminho = os.path.join(pastaResultados,subpastaArquivos)

            #caminho_arquivo_resultadosVelSub = os.path.join(caminho, f"velSub.csv")

            #caminho_arquivo_resultadosVelDes = os.path.join(caminho, f"velDes.csv")

            #csv_VelSub = []

            #csv_VelDes = []

            """for velocidadeSubida in self.arrayDasArraysVelSub[i]:

                csv_VelSub.append(velocidadeSubida)"""

            #dfVelSub = pd.DataFrame(csv_VelSub, columns=["Velocidade de subida"])

            #dfVelSub.to_csv(caminho_arquivo_resultadosVelSub, sep="\t", index=True)

            """for velocidadeDescida in self.arrayDasArraysVelDes[i]:

                csv_VelDes.append(velocidadeDescida)"""

            #dfVelDes = pd.DataFrame(csv_VelDes, columns=[ "Velocidade de descida"])

            #dfVelDes.to_csv(caminho_arquivo_resultadosVelDes, sep="\t", index=True)

            #print(f"\nVelocidades de cada grupo salvas para o arquivo {arrayNomesTxt[i]} em {caminho}\n")

            #print(f"\nÁnalise do arquivo {arrayNomesTxt[i]} finalizada\n")

        """estatisticas = {
            "nome": arrayNomesTxt,
            "mediaVelSub": self.arrayMediaVelSub,
            "desvPadVelSub": self.arrayDesvPadAmostVelSub,
            "media_DesvPadVelSub_Erro": self.arrayDesvPadAmostMediaVelSub,
            "mediaVelDes": self.arrayMediaVelDes,
            "desvPadVelDes": self.arrayDesvPadAmostVelDes,
            "media_DesvPadVelDes_Erro": self.arrayDesvPadAmostMediaVelDes
        }"""

        time.sleep(0.5)
        self.atualizar_progresso(100, "Completo")
        time.sleep(0.5)

        #dataFrameEstatisticas = pd.DataFrame(estatisticas)

        #caminho_arquivo_estatisticas = os.path.join(pastaResultados, "estatisticas.csv")

        #dataFrameEstatisticas.to_csv(caminho_arquivo_estatisticas, sep="\t", index=True)

        #print(f"\nEstatísticas de todos os grupos reunidas em {caminho_arquivo_estatisticas}\n")

    def cancelarOsCalculosFeitos(self):

        # Precisa limpar as arrays e abrir novamente 
        # a janela principal fechando a de executar 
        # voltando ao estado inicial

        self.arrayDasArraysVelSub = []

        self.arrayDasArraysVelDes = []

        self.arrayDasArraysVelSubInstantes = []

        self.arrayDasArraysVelDesInstantes = []

        self.arrayDesvPadAmostVelSub = []

        self.arrayDesvPadAmostVelDes = []

        self.arrayMediaVelSub = []

        self.arrayMediaVelDes = []

        self.arrayDesvPadAmostMediaVelDes = []

        self.arrayDesvPadAmostMediaVelSub = []

        self.arrayCaminhosArquivos = None

        self.diretorio = None
        
        self.voltagem = None

        self.densGot = None

        self.distPlacs = None

        self.varredura = 5

        self.janelaAtribuicao.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        self.janela_execucao.hide()

        self.janela_atribuicao.show()

        self.janela_execucao.close()

    def classificarVelocidades(self, dataFrameVelocidades, indice_i):

        i = indice_i

        # Retorna o número de linhas

        quantidadeLinhas = dataFrameVelocidades.shape[0]

        def atribuicaoVelocidadeDescida():

                self.arrayDasArraysVelDes[i].append(velocidade)

                self.arrayDasArraysVelDesInstantes[i].append(instante)

        def atribuicaoVelocidadeSubida():

            self.arrayDasArraysVelSub[i].append(velocidade)

            self.arrayDasArraysVelSubInstantes[i].append(instante)


        for j in range(quantidadeLinhas):

            velocidade = dataFrameVelocidades.iloc[j,1]

            instante = dataFrameVelocidades.iloc[j,0]

            # Primeiro, vamos descobrir se o ponto analisado 
            # vai estar em um dos extremos ou no meio

            if velocidade == 0:
                
                Pontuacao = self.varrerDianteira(dataFrameVelocidades, quantidadeLinhas, j)

                if Pontuacao > 0:

                    atribuicaoVelocidadeSubida()

                elif Pontuacao < 0:

                    atribuicaoVelocidadeDescida()

                elif Pontuacao == 0:

                    pass

            elif velocidade != 0 and velocidade != (quantidadeLinhas-1):

                PontuacaO = self.varrerDianteira(dataFrameVelocidades, quantidadeLinhas, j) + self.varrerTraseira(dataFrameVelocidades, j)

                if PontuacaO > 0:

                    atribuicaoVelocidadeSubida()

                elif PontuacaO < 0:

                    atribuicaoVelocidadeDescida()

                elif PontuacaO == 0:

                    pass

            elif velocidade == (quantidadeLinhas-1):

                pontuacaO = self.varrerTraseira(dataFrameVelocidades, j)

                if pontuacaO > 0:

                    atribuicaoVelocidadeSubida()

                elif pontuacaO < 0:

                    atribuicaoVelocidadeDescida()

                elif pontuacaO == 0:

                    pass

    def varredor(self, vel):

        velocidade = vel

        ponto = 0

        if velocidade > 0:

            ponto += 1

        elif velocidade < 0:

            ponto += -1

        elif velocidade == 0:

            ponto += 0

        return ponto
                    
    def varrerDianteira(self, dataFrameVelocidades, quantidadeLinhas, indice_j):
        
        pontuacao = 0

        j = indice_j

        indice = dataFrameVelocidades.index[j]

        diferenca = (quantidadeLinhas-1) - indice

        if diferenca <= self.varredura:

            exclusao = self.varredura - diferenca

            for k in range((self.varredura+1)-exclusao):

                pontuacao += self.varredor(dataFrameVelocidades.iloc[(j+k),1])

        else:

            for k in range(self.varredura+1):

                pontuacao += self.varredor(dataFrameVelocidades.iloc[(j+k),1])

        return pontuacao


    def varrerTraseira(self, dataFrameVelocidades, indice_j):

        j = indice_j

        pontuacao = 0

        indice = dataFrameVelocidades.index[j]

        diferenca = self.varredura - indice

        if abs(diferenca) <= self.varredura:

            exclusao = self.varredura - diferenca

            for k in range((self.varredura+1)-exclusao):

                pontuacao += self.varredor(dataFrameVelocidades.iloc[(j-k),1])

        else:

            for k in range(self.varredura+1):

                pontuacao += self.varredor(dataFrameVelocidades.iloc[(j-k),1])

        return pontuacao

        # MÉTODOS DE EDIÇÃO #

        # MÉTODOS DE AVALIAÇÃO #


    
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