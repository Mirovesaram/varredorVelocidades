# Eu sinceramente não queria criar mais uma vez
# script main que centraliza todos os métodos e
# classes que movimentam as janelas justamente 
# para melhorar a escalabilidade do código e sua 
# organização. Contudo, por questões de tempo não
# pude estudar a implementação correta e conexão
# dos diversos scripts com seus métodos separados.
# Por isso, infelizmente mais uma vez seguirei essa
# prática que mais atrapalha do que ajuda. Mas dessa
# vez estou tentando utilizar comentários de maneira
# mais ostensiva para tentar facilicitar a organização
# do código

import logging

from findpeaks import findpeaks

import os

import sys

import traceback

import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolBar

from matplotlib.figure import Figure

from matplotlib.ticker import MultipleLocator 

import matplotlib.colors as mcolors

import numpy as np

import glob

import time

import math

from PyQt5.QtWidgets import QMainWindow, QFrame, QMenu, QApplication, QFileDialog, QMessageBox, QCheckBox, QHBoxLayout, QVBoxLayout, QWidget

from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import QAbstractTableModel, Qt, QPoint

from PyQt5.QtGui import QIcon

from interfaceGerada.janelaAtribuicao import Ui_janelaAtribuicao

from interfaceGerada.janelaExecucao import Ui_MainWindowExecucao

from interfaceGerada.janelaAvaliacao import Ui_MainWindowAvaliacao  

from interfaceGerada.janelaDetalhes import Ui_MainWindowJanelaDetalhes

#####################
#####################
# MÉTODOS POPULARES # -> São utilizados por
#####################    mais de uma janela
#####################

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

    # Por ser uma QMessageBox(), não haverá como
    # aplicar redimentsionamento.
    
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
    erro.setWindowIcon(QIcon(resource_path(r'icones\logoAlternativa.ico')))
    
    # E os detalhes do erro, como onde
    # ocorreu nas linhas de código
    erro.setDetailedText(mensagemErro)
    
    # Comando para quando fechar a caixa, encerrar o programa
    erro.exec_()

# A função dessa classe é preparar um dataframe para exibição
# de seus dados em uma tabela recebendo o dataframe (def __init__), 
# contando o número de linhas (def rowCount) e de colunas (def columnCount), 
# lendo e dispondo os dados em string a fim de garantir que todo tipo 
# de dado seja exibido na tabela em sua devida linha e coluna (def data) 
# e lendo os cabeçalhos para exibir devidamente na coluna bem como verificando 
# se a disposição deles é vertical ou horizontal. Ou seja, saber se os nomes 
# das colunas estarão na primeira linha da tabela ou na primeira coluna 
# da tabela, respectivamente, por assim dizer (def headerData)
class PandasModel(QAbstractTableModel):

    def __init__(self, dataframe):
        super().__init__()
        self._data = dataframe

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data.iat[index.row(), index.column()]
            return str(value)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QMainWindow, Ui_janelaAtribuicao):
            
    def __init__(self):

        super().__init__()

        self.setupUi(self)

        # Configuração do ícone
        self.setWindowIcon(QIcon(resource_path(r"icones\logoAlternativa.ico")))

        # Inserindo a logo do Facillikan
        self.labelLogoFacillikan.setPixmap(QtGui.QPixmap(resource_path(r'icones\logoAlternativa3.ico')))

        # Inicialização do objeto janela de atribuição
        self.janela_atribuicao = QMainWindow()

        self.janelaAtribuicao = Ui_janelaAtribuicao()

        self.janelaAtribuicao.setupUi(self.janela_atribuicao)

        # Inicialização do objeto janela de execução
        self.janela_execucao = QMainWindow()

        self.janelaExecucao = Ui_MainWindowExecucao()

        self.janelaExecucao.setupUi(self.janela_execucao)

        # Inicialização do objeto janela de avaliação
        self.janela_avaliacao = QMainWindow()

        self.janelaAvaliacao = Ui_MainWindowAvaliacao()

        self.janelaAvaliacao.setupUi(self.janela_avaliacao)

        # Inicialização do objeto janela de edição
        self.janela_detalhes = QMainWindow()

        self.janelaDetalhes = Ui_MainWindowJanelaDetalhes()

        self.janelaDetalhes.setupUi(self.janela_detalhes)

        # Estabelecimento de objetos já pré-existentes

        self.doubleSpinBox_voltagem.setEnabled(False)

        self.imgInvertida = self.checkBoxImagemInvertida 

        self.progressBar = self.janelaExecucao.progressBarExecucao

        self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        self.layout = self.janelaAvaliacao.gridLayout_Grafico

        self.layoutDetalhes = self.janelaDetalhes.gridLayoutGrafico

        self.checkBoxBarraErro = self.janelaAvaliacao.checkBoxBarraErro

        self.checkBoxBarraErro.stateChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.tabela = self.janelaAvaliacao.tabelaGotas

        self.tabela.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tabela.customContextMenuRequested.connect(self.abrirMenuContexto)

        self.dSpinBoxCargElemnt = self.janelaAvaliacao.doubleSpinBoxCargElement

        self.dSpinBoxCargElemnt.valueChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.pushButtonSalvarVels = self.janelaAvaliacao.pushButtonBaixarVels

        self.pushButtonSalvarVels.clicked.connect(self.escolherPastaSaveVelsGotas)

        self.pushButtonSalvarDados = self.janelaAvaliacao.pushButtonBaixarDf

        self.pushButtonSalvarDados.clicked.connect(self.escolherPastaSaveDadosGotas)

        self.pushButtonSelecPasta.clicked.connect(self.buscarDirArquivosTxt)

        self.pushButton_executar.clicked.connect(self.extrairVariaveis)

        self.janelaAvaliacao.pushButtonRefazerCalculos.clicked.connect(self.reinicializar)

        self.janelaAvaliacao.checkBoxRetirarMultiplos.stateChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.janelaAvaliacao.checkBoxExcluiCargaPorErro.stateChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.janelaAvaliacao.doubleSpinBoxErroLimite.valueChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.janelaAvaliacao.doubleSpinBoxLarguraCompartimento.valueChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.janelaAvaliacao.pushButtonSalvarDadosHistograma.clicked.connect(self.escolherPastaSaveDadosHist)

        #############
        #############
        # ATRIBUTOS #
        #############
        #############

        # Atributo para definir se o checkBox da
        # janela de atribuição foi checkado ou não
        #self.inverteu = 0

        # "Array 2D" que vai armazenar os caminhos de cada voltagem
        self.arrayArrayPaths = []

        # Array que vai armazenar as voltagens
        self.arrayVoltagens = []

        # Array 2D dos nomes dos arquivos por voltagem
        self.arrArrsNomFileP_Voltgm = []

        # Array das arrays de velocidades de subida e descida
        self.arrArrArrsVelSubP_Vltgm = []

        self.arrArrArrsVelDesP_Vltgm = []

        # Array das arrays de velocidades desconsideradas
        self.arrArrArrsVelP_VltgmNull = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades de subida e descida
        self.arrArrArrsVelSubP_VltgmInsts = []

        self.arrArrArrsVelDesP_VltgmInsts = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades desconsideradas
        self.arrArrArrsVelP_VltgmNullInsts = []

        # Array de desvios padrões amostrais das velocidades 
        # de subida e descida
        self.arrArrsDesvPadAmostVelSubP_Vltgm = []

        self.arrArrsDesvPadAmostVelDesP_Vltgm = []

        #Array de médias das velocidades de subida e descida
        self.arrArrsMedVelSubP_Vltgm = []

        self.arrArrsMedVelDesP_Vltgm = []

        # Array de desvios padrões amostrais da média de (erros) 
        # velocidades de subida e descida
        self.arrArrsDesvPadAmostMedVelDesP_Vltgm = []

        self.arrArrsDesvPadAmostMedVelSubP_Vltgm = []

        # Arrays das cargas, raios (E seus erros) 
        # das gotas (E por fim, os erros relativos)
        self.arrArrsCargasP_Vltgm = []

        self.arrArrsErrCargasP_Vltgm = []

        self.arrArrsPorctErrCargasP_Vltgm = []

        self.arrArrsRaiosP_Vltgm = []

        self.arrArrsErrRaiosP_Vltgm = []

        self.arrArrsPorctErrRaiosP_Vltgm = []

        # Array das classificações das gotas
        self.arrArrsClassifGotP_Vltgm = []

        # Array da estrutura dos checkboxes para considerar as gotas
        self.arrArrsCheckBoxesP_Vltgm = []

        # Array para as gotas desconsideradas no caso de imagem
        # invertida (O nome delas no caso)
        self.arrayGotaNull = []

        # Array para as gotas desconsideradas no caso de falta
        # de quantidade de pontos de velocidade suficiente para
        # cálculos estatísticos
        self.arrayGotaNullPorVel = []

        # Esse dado vai ser somente utilizado como
        # modelo para tabela
        self.dataFrameTabela = None

        # Essa array irá armazenar diferentes dataframes
        # por voltagem
        self.arrDfP_Vltgm = []

        # Inicialização do atributo diretório
        self.diretorio = None

        # Inicialização do atributo densidade da gota
        self.densGot = None

        # Inicialização do atributo distância das placas
        self.distPlacs = None

        # Inicialização do atributo varredura
        self.varredura = 5

        # Inicialização da constante 1
        self.constante1 = None

        # Inicialização da constante 2
        self.constante2 = None

        # Valor da viscosidade do ar utilizado 
        self.viscosidadeAr = None

        # Valor da gravidade [m*s^-2]
        self.gravidade = 9.80665

        # Densidade do ar [Kg*m^-3]
        self.densidadeAr_p2 = None

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
        
        else:

            self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

    def separarCaminhos(self, arrayCaminhosTxt):

        # Aqui temos os caminhos ordenados
        arrayCaminhosTxtOrden = sorted(arrayCaminhosTxt)

        # Aqui temos os nomes dos arquivos ordenados
        nomesArquivosTxtOrden = [os.path.splitext(os.path.basename(item))[0] for item in arrayCaminhosTxtOrden]

        numeroRepeticoes = len(arrayCaminhosTxtOrden)

        # Sua função é armazenar os valores de voltagem que apareceram
        arrayVoltagens = []

        for i in range(numeroRepeticoes):
            
            # O primeiro elemento deve ter sua voltagem adicionada obrigatoriamente
            if i == 0:
                
                try: 

                    # Ler os 3 primeiros caracteres
                    # e verificar se formam um número
                    voltagem = int(nomesArquivosTxtOrden[i][:3].strip())

                except Exception as e:
                    
                    caracteres = nomesArquivosTxtOrden[i][:3]

                    # Imprimir os caracteres reais
                    caracteres_repr = repr(caracteres)
                    
                    self.arrayArrayPaths = []

                    self.arrayVoltagens = []

                    self.arrArrsNomFileP_Voltgm = []

                    raise ValueError(f"O ARQUIVO {nomesArquivosTxtOrden[i]} ESTÁ EM UM FORMATO INAPROPRIADO.\n"
                                     f"{caracteres_repr} NÃO É UM NÚMERO.\n"
                                     "Os 3 primeiros caracteres devem corresponder ao valor de voltagem.\n"
                                     "Ou seja, o arquivo pode ter qualquer nome, o importante é que esse nome inicie\n"
                                     "com o valor de voltagem. Por exemplo, se você tem um arquivo de uma\n"
                                     "gota que foi registrada com uma voltagem de 50 V, o nome do arquivo\n"
                                     "tem que começar com 050. Logo:\n"
                                     "050PodeVirQualquerCoisaDepois.txt (Correto)\n"
                                     "Não pode ser:\n"
                                     "50PodeVirQualquerCoisaDepois.txt (Errado)\n"
                                     "Nem pode:\n"
                                     "QualquerCoisa.txt (Errado)")
                
                # Adiciona esse valor de voltagem
                arrayVoltagens.append(voltagem)

                # Adiciona a primeira array de caminhos 
                # para a voltagem
                self.arrayArrayPaths.append([])

                # Adiciona como primeiro item o valor de 
                # voltagem dessa array
                self.arrayArrayPaths[i].append(voltagem)
                
                # Adiciona em seguida o caminho
                self.arrayArrayPaths[i].append(arrayCaminhosTxtOrden[i])

                # Adiciona a primeira array de nomes 
                # para a voltagem
                self.arrArrsNomFileP_Voltgm.append([])

                # Agora adiciona o nome à primeira array
                self.arrArrsNomFileP_Voltgm[i].append(nomesArquivosTxtOrden[i])
            
            # Os próximos elementos devem ser avaliados para ver se apresentam
            # correspondência com alguma voltagem
            else:
                
                try:

                    # Ler os 3 primeiros caracteres
                    # e verificar se formam um número
                    voltagem = int(nomesArquivosTxtOrden[i][:3].strip())

                except Exception as e:

                    self.arrayArrayPaths = []

                    self.arrayVoltagens = []

                    self.arrArrsNomFileP_Voltgm = []

                    caracteres = nomesArquivosTxtOrden[i][:3]

                    caracteres_repr = repr(caracteres)

                    raise ValueError(f"O ARQUIVO {nomesArquivosTxtOrden[i]} ESTÁ EM UM FORMATO INAPROPRIADO.\n"
                                     f"{caracteres_repr} NÃO É UM NÚMERO.\n"
                                     "Os 3 primeiros caracteres devem corresponder ao valor de voltagem.\n"
                                     "Ou seja, o arquivo pode ter qualquer nome, o importante é que esse nome inicie\n"
                                     "com o valor de voltagem. Por exemplo, se você tem um arquivo de uma\n"
                                     "gota que foi registrada com uma voltagem de 50 V, o nome do arquivo\n"
                                     "tem que começar com 050. Logo:\n"
                                     "050PodeVirQualquerCoisaDepois.txt (Correto)\n"
                                     "Não pode ser:\n"
                                     "50PodeVirQualquerCoisaDepois.txt (Errado)\n"
                                     "Nem pode:\n"
                                     "QualquerCoisa.txt (Errado)")
                
                # Avalia qual o tamanho da array
                # para poder obter o endereço do
                # último item
                qtdVoltgs = len(arrayVoltagens)

                # Como os caminhos estão ordenados, os caminhos
                # de certa voltagem serão todos adicionados. Quando
                # aparecer uma voltagem diferente, isso indica que
                # já é para criar mais uma array e adicionar os
                # caminhos somente dessa nova voltagem
                if voltagem == arrayVoltagens[qtdVoltgs-1]:

                    self.arrayArrayPaths[qtdVoltgs-1].append(arrayCaminhosTxtOrden[i])

                    self.arrArrsNomFileP_Voltgm[qtdVoltgs-1].append(nomesArquivosTxtOrden[i])

                else:

                    arrayVoltagens.append(voltagem)

                    self.arrayArrayPaths.append([])

                    self.arrayArrayPaths[qtdVoltgs].append(voltagem)

                    self.arrayArrayPaths[qtdVoltgs].append(arrayCaminhosTxtOrden[i])

                    self.arrArrsNomFileP_Voltgm.append([])

                    self.arrArrsNomFileP_Voltgm[qtdVoltgs].append(nomesArquivosTxtOrden[i])

        self.arrayVoltagens = arrayVoltagens

    def lerDiretorio(self, diretorio):

        arrayCaminhosTxt = []

        self.diretorio = diretorio

        extensaoArquivo = '*.txt'

        buscaDosTxts = os.path.join(self.diretorio, extensaoArquivo)

        arrayCaminhosTxt = glob.glob(buscaDosTxts)

        if arrayCaminhosTxt != []:

            self.separarCaminhos(arrayCaminhosTxt)

            for i in range(len(self.arrayVoltagens)):

                self.executarCalculos(enderecoVoltagem=i)
            
            self.prepararTabelaGraficoHistograma()

        else:
            
            QMessageBox.warning(self, "Erro", "A pasta que você escolheu não tem nenhum arquivo .txt")

    # Método para verificar se tudo foi devidamente 
    # preenchido e então extrair as variáveis para
    # executar os cálculos

    def extrairVariaveis(self):
            
        densGot = self.doubleSpinBoxDensGot.value()

        distPlacs = self.doubleSpinBox_distPlacs.value()

        viscosAr = self.doubleSpinBoxViscosidadeAr.value()

        densAr = self.doubleSpinBoxDensidadeAr.value()

        #voltagem = self.doubleSpinBox_voltagem.value()

        #if densGot != 0 and voltagem != 0 and distPlacs != 0:

        if densGot != 0 and distPlacs != 0 and densAr != 0 and viscosAr != 0:
    
            if self.diretorio:

                #self.voltagem = voltagem

                self.densGot = densGot

                self.distPlacs = distPlacs

                self.densidadeAr_p2 = densAr

                self.viscosidadeAr = viscosAr * 10**(-5)

                #if self.imgInvertida.isChecked() == True:
             
                    #self.inverteu = 1

                # Para fins de teste

                #print(f"{voltagem}, {distPlacs}, {densGot}")

                self.lerDiretorio(self.diretorio)

            else:

                QMessageBox.warning(self, "Erro", "Você não escolheu uma pasta.")
        
        else:
            
            QMessageBox.warning(self, "Erro", "Preencha os campos corretamente. Algum deles está nulo.")

    #######################
    #######################
    # MÉTODOS DE EXECUÇÃO #
    #######################
    #######################

    # Método de atualização da barra de progresso

    def atualizar_progresso(self, valor, mensagem):

        # Altera o valor de porcentagem da barra
        self.progressBar.setValue(int(valor))

        # Altera o texto que acompanha
        self.progressBar.setFormat(f"{mensagem} ({int(valor)}%)")

        # Comando para atualização da UI em tempo real, 
        # sem ser feito somente ao fim
        QApplication.processEvents()

    # O objetivo desse método é estabelecer os conjuntos iniciais,
    # ele só será para estabelecimento inicial dos resultados e outros
    # métodos se encarregarão de editar esses dados inicialmente 
    # estabelecidos aqui
    def executarCalculos(self, enderecoVoltagem):

        # Processo para transicionar entre janelas

        # Esconde a anterior
        self.hide()
        
        # Mostra a próxima
        self.janela_execucao.show()

        self.janela_execucao.setWindowIcon(QIcon(resource_path(r"icones\logoAlternativa.ico")))
        
        self.atualizar_progresso(10, f"Iniciando processamento para {self.arrayVoltagens[enderecoVoltagem]}V")
        
        # Vou fazer uma iteração global do algoritmo que é
        # regida pelo número de arquivos txt presentes na array.
        # da voltagem em análise
        numeroDeRepeticoes = len(self.arrayArrayPaths[enderecoVoltagem])

        # Estabelecimento das arrays para a voltagem em análise
        self.arrArrArrsVelSubP_Vltgm.append([])

        self.arrArrArrsVelDesP_Vltgm.append([])

        self.arrArrArrsVelP_VltgmNull.append([])

        self.arrArrArrsVelSubP_VltgmInsts.append([])

        self.arrArrArrsVelDesP_VltgmInsts.append([])

        self.arrArrArrsVelP_VltgmNullInsts.append([])

        self.arrArrsDesvPadAmostVelSubP_Vltgm.append([])

        self.arrArrsDesvPadAmostVelDesP_Vltgm.append([])

        self.arrArrsMedVelSubP_Vltgm.append([])

        self.arrArrsMedVelDesP_Vltgm.append([])

        self.arrArrsDesvPadAmostMedVelSubP_Vltgm.append([])

        self.arrArrsDesvPadAmostMedVelDesP_Vltgm.append([])

        self.arrArrsCargasP_Vltgm.append([])

        self.arrArrsErrCargasP_Vltgm.append([])

        self.arrArrsPorctErrCargasP_Vltgm.append([])

        self.arrArrsRaiosP_Vltgm.append([])

        self.arrArrsErrRaiosP_Vltgm.append([])

        self.arrArrsPorctErrRaiosP_Vltgm.append([])

        self.arrArrsClassifGotP_Vltgm.append([])

        self.arrArrsCheckBoxesP_Vltgm.append([])

        self.arrDfP_Vltgm.append([]) 
        
        self.atualizar_progresso(20, f"Calculando as constantes para {self.arrayVoltagens[enderecoVoltagem]}V")
        
        # Configuração das constantes
        self.constante1 = (9/2)*(math.pi)*(self.distPlacs)*math.sqrt((self.viscosidadeAr**3)/(self.gravidade*(self.densGot-self.densidadeAr_p2)))

        self.constante2 = (3/2)*math.sqrt((self.viscosidadeAr)/(self.gravidade*(self.densGot-self.densidadeAr_p2)))
      
        self.atualizar_progresso(30, f"Iniciando Varredura para {self.arrayVoltagens[enderecoVoltagem]}V")    

        # Definição padrão do alcance de varredura
        self.varredura = 5

        for i in range(1,numeroDeRepeticoes,1):

            # Estabelecimento das arrays para a array recém adicionada

            self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem].append([])

            self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem].append([])

            self.arrArrArrsVelP_VltgmNull[enderecoVoltagem].append([])

            self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem].append([])

            self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem].append([])

            self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem].append([])

            txtEmAnalise = self.arrayArrayPaths[enderecoVoltagem][i]

            # Isso é feito para garantir que caso 
            # ocorra um erro por causa da estrutura 
            # do dataframe, o usuário seja informado 
            # mais facilmente
            try:
                
                # O parâmetro usecols (Não tem mais) garante que as únicas colunas 
                # utilizadas sejam as das strings entregues e o 
                # parâmetro header coloca a segunda linha (linha 1) 
                # como cabeçalho da tabela ignorando a primeira 
                # linha que no nosso contexto nos atrapalha e o 
                # parâmetro sep indica a separação entre os dados, 
                # onde "\t" indica que ela é feita com tab 
                # (Tabulação)
                dataFrameVelocidades = pd.read_csv(txtEmAnalise, sep="\t", header=1, names=['t','vy'])

            except Exception as e:

                 raise ValueError(f"O dataframe do arquivo {txtEmAnalise} apresenta problemas")

            # dropna é uma função que exclui linhas onde há dados
            # ausentes (NaN)
            dataFrameVelocidades = dataFrameVelocidades.dropna()

            self.classificarVelocidades(dataFrameVelocidades=dataFrameVelocidades, enderecoGota=(i-1), enderecoVoltagem=enderecoVoltagem)

            # Aqui já é separado as velocidades numa primeira
            # classificação do varredor. Agora precisamos reorganizar
            # considerando o desvio padrão atual e a média atual

            desvPadAmostDes = np.std(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1], ddof=1)
            
            medVelDes = np.mean(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1])

            for i2 in reversed(range(len(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1]))):

                velDes = self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1][i2]

                if not ((medVelDes - desvPadAmostDes) <= velDes <= (medVelDes + desvPadAmostDes)):

                    velDesconsid = self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1].pop(i2)

                    velDesconsidInst = self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem][i-1].pop(i2)

                    self.arrArrArrsVelP_VltgmNull[enderecoVoltagem][i-1].append(velDesconsid)

                    self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem][i-1].append(velDesconsidInst)

            desvPadAmostSub = np.std(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1], ddof=1)

            medVelSub = np.mean(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1])

            for i3 in reversed(range(len(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1]))):

                velDes = self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1][i3]

                if not ((medVelSub - desvPadAmostSub) <= velDes <= (medVelSub + desvPadAmostSub)):

                    velDesconsid = self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1].pop(i3)

                    velDesconsidInst = self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem][i-1].pop(i3)

                    self.arrArrArrsVelP_VltgmNull[enderecoVoltagem][i-1].append(velDesconsid)

                    self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem][i-1].append(velDesconsidInst)

            # Configuração inicial dos resultados 
            # para os conjuntos de velocidade, suas médias, 
            # seus desvios padrão amostrais e seus erros
            desvioPadraoAmostralVelocidadeDescida = np.std(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1], ddof=1)

            desvioPadraoAmostralVelocidadeSubida = np.std(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1], ddof=1)

            self.arrArrsDesvPadAmostVelSubP_Vltgm[enderecoVoltagem].append(desvioPadraoAmostralVelocidadeSubida)

            self.arrArrsDesvPadAmostVelDesP_Vltgm[enderecoVoltagem].append(desvioPadraoAmostralVelocidadeDescida)

            self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem].append(np.mean(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1]))

            self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem].append(np.mean(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1]))

            self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem].append(desvioPadraoAmostralVelocidadeDescida/(math.sqrt(len(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i-1]))))

            self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem].append(desvioPadraoAmostralVelocidadeSubida/(math.sqrt(len(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i-1]))))  

        # Precisamos agora excluir gotas que obtiveram valores estatísticos com menos
        # de 10 pontos de velocidade de subida ou descida. Essas gotas não tem valores
        # estatísticos confiáveis

        self.atualizar_progresso(40, f'Excluindo gotas com quantidade insuficiente de pontos de velocidade')

        # Essa parte de exclusão não pode ser colocada dentro do laço de repetição i
        # pois precisamos de todos as gotas já analisadas para exclui-las. Excluir
        # enquanto se analise resulta em erros

        for j in reversed(range(numeroDeRepeticoes)):

            # Gota em análise tanto pela sua tabela de velocidades
            # de subida quanto pela sua tabela de velocidades de descida

            gotaDes = self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][j-1]

            gotaSub = self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][j-1]

            testeDes = len(gotaSub)

            testeSub = len(gotaDes)

            # Se a quantidade de pontos de velocidade de subida ou de
            # descida for menor que ou igual a 10. Exclua a gota e registre
            # sua exclusão

            if (len(gotaDes) <= 10) or (len(gotaSub) <= 10):

                self.arrayGotaNullPorVel.append(self.arrArrsNomFileP_Voltgm[enderecoVoltagem][j-1])

                self.arrayArrayPaths[enderecoVoltagem].pop(j-1)

                self.arrArrsNomFileP_Voltgm[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelP_VltgmNull[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem].pop(j-1)

                self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem].pop(j-1)

                self.arrArrsDesvPadAmostVelSubP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrsDesvPadAmostVelDesP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem].pop(j-1)

                self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem].pop(j-1)

        # Atualize o número de repetições
        numeroDeRepeticoes = len(self.arrayArrayPaths[enderecoVoltagem])

        self.atualizar_progresso(45, f"Calculando os valores de carga e raio das gotas e seus erros para {self.arrayVoltagens[enderecoVoltagem]}V")

        # Calculando as cargas, os raios e seus erros
        for k in range(0,numeroDeRepeticoes-1,1):

            resultado = self.calcularCargaRaioGota(enderecoVoltagem=enderecoVoltagem, enderecoGota=k)

            if resultado is not None:

                # É necessário fazer dessa maneira pois colocar o .append no próprio
                # método de cálculos do raio e carga é problemático.
                self.arrArrsCargasP_Vltgm[enderecoVoltagem].append(resultado[0])

                self.arrArrsRaiosP_Vltgm[enderecoVoltagem].append(resultado[1])

                self.arrArrsErrCargasP_Vltgm[enderecoVoltagem].append(resultado[2])

                self.arrArrsErrRaiosP_Vltgm[enderecoVoltagem].append(resultado[3])

                self.arrArrsPorctErrCargasP_Vltgm[enderecoVoltagem].append(resultado[4])

                self.arrArrsPorctErrRaiosP_Vltgm[enderecoVoltagem].append(resultado[5])

        # Perceba aqui que esse método de exclusão em conjunção com o método calcularCargaRaioGota
        # não é tão simples como o que foi executado mais acima com o laço de repetição no sentido
        # de contagem regressiva (Começando do fim para o início) e utilizando o método .pop()

        self.arrayArrayPaths[enderecoVoltagem] = [item for item in self.arrayArrayPaths[enderecoVoltagem] if item != None]

        self.arrArrsNomFileP_Voltgm[enderecoVoltagem] = [item for item in self.arrArrsNomFileP_Voltgm[enderecoVoltagem] if item != None]

        self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrArrsVelP_VltgmNull[enderecoVoltagem] = [item for item in self.arrArrArrsVelP_VltgmNull[enderecoVoltagem] if item != None]

        self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem] = [item for item in self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem] if item != None]

        self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem] = [item for item in self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem] if item != None]

        self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem] = [item for item in self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem] if item != None]

        self.arrArrsDesvPadAmostVelSubP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsDesvPadAmostVelSubP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrsDesvPadAmostVelDesP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsDesvPadAmostVelDesP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem] if item != None]

        self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem] = [item for item in self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem] if item != None]

        self.atualizar_progresso(50, f"Classificando as gotas para {self.arrayVoltagens[enderecoVoltagem]}V")

        # Atualiza o número de repetições
        numeroDeRepeticoes = len(self.arrayArrayPaths[enderecoVoltagem])

        for l in range(numeroDeRepeticoes-1):

            self.arrArrsClassifGotP_Vltgm[enderecoVoltagem].append(self.classificarGota(enderecoGota=l, enderecoVoltagem=enderecoVoltagem))

        self.atualizar_progresso(60, f"Criando e configurando os check-boxes para {self.arrayVoltagens[enderecoVoltagem]}V")

        for m in range(numeroDeRepeticoes-1):

            self.arrArrsCheckBoxesP_Vltgm[enderecoVoltagem].append(self.criarCheckBoxes(enderecoCheckBox=m, enderecoVoltagem=enderecoVoltagem))

        self.atualizar_progresso(70, f"Criando os dataframes de dados para {self.arrayVoltagens[enderecoVoltagem]}V")

        baseParaDf = {
            "Nome da gota": self.arrArrsNomFileP_Voltgm[enderecoVoltagem],
            "Qualidade da gota": self.arrArrsClassifGotP_Vltgm[enderecoVoltagem],
            "Carga (C)": self.arrArrsCargasP_Vltgm[enderecoVoltagem],
            "Erro relativo (%) (C)": [x * 100 for x in self.arrArrsPorctErrCargasP_Vltgm[enderecoVoltagem]],
            "Raio (m)": self.arrArrsRaiosP_Vltgm[enderecoVoltagem],
            "Erro relativo (%) (m)": [x * 100 for x in self.arrArrsPorctErrRaiosP_Vltgm[enderecoVoltagem]]
        }

        self.arrDfP_Vltgm[enderecoVoltagem] = pd.DataFrame(baseParaDf)

    # Métodos de cálculo de carga e raio de dada gota i
    def calcularCargaRaioGota(self, enderecoVoltagem, enderecoGota):

        velDes = self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem][enderecoGota]

        velSub = self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem][enderecoGota]

        constante1 = self.constante1

        constante2 = self.constante2

        voltagem = self.arrayVoltagens[enderecoVoltagem]
        
        soma = abs(velDes) + abs(velSub)

        diferenca = abs(velDes) - abs(velSub)

        if self.imgInvertida.isChecked() == True:

            diferenca = abs(velSub) - abs(velDes)

        desvPadAmostMediaVelDes = self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem][enderecoGota]

        desvPadAmostMediaVelSub = self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem][enderecoGota]

        resultados = []

        # Se a velocidade de subida está maior que a
        # de descida e não seja uma imagem invertida,
        # pode ser entrada de ar.
        if diferenca < 0:

            self.arrayGotaNull.append(self.arrArrsNomFileP_Voltgm[enderecoVoltagem][enderecoGota])

            self.arrayArrayPaths[enderecoVoltagem][enderecoGota+1] = None

            self.arrArrsNomFileP_Voltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelP_VltgmNull[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem][enderecoGota] = None

            self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem][enderecoGota] = None

            self.arrArrsDesvPadAmostVelSubP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrsDesvPadAmostVelDesP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrsMedVelSubP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrsMedVelDesP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrsDesvPadAmostMedVelSubP_Vltgm[enderecoVoltagem][enderecoGota] = None

            self.arrArrsDesvPadAmostMedVelDesP_Vltgm[enderecoVoltagem][enderecoGota] = None

            return None
        
        razao = (constante1)/(2*voltagem)

        primeiraParte = 2*razao*math.sqrt(diferenca)

        segundaParte = (soma*razao)/(math.sqrt(diferenca))

        parteAbs = (constante2)/(2*math.sqrt(diferenca))
        
        """TESTE DE APLICAÇÃO DA CORREÇÃO"""

        interruptor = 0

        """Versão oficial sem correção"""
        if interruptor == 0:

            carga = 2*razao*soma*math.sqrt(diferenca)

            erroCarga = (abs(primeiraParte+segundaParte)*desvPadAmostMediaVelDes)+(abs(primeiraParte-segundaParte)*desvPadAmostMediaVelSub)

            raio = constante2*math.sqrt(diferenca)

            erroRaio = (abs(parteAbs)*desvPadAmostMediaVelDes)+(abs(-parteAbs)*desvPadAmostMediaVelSub)

        """Versão não oficial com correção"""
        if interruptor == 1:
        
            constanteB = 8.2 * 10**(-3) # Pa * m

            pressaoAtmosferica = 89236.67 # Pa

            difDens = self.densGot - self.densidadeAr_p2

            segundaParteInterna = (9/4)*(self.viscosidadeAr/self.gravidade)*(1/(difDens))

            primeiraParteInterna = constanteB/(2*pressaoAtmosferica)

            raio = math.sqrt((primeiraParteInterna**2) + segundaParteInterna*diferenca) - primeiraParteInterna

            parteExterna = (4/3)*math.pi*((self.gravidade*self.distPlacs)/(voltagem))*difDens

            carga = parteExterna*((soma)/(diferenca))*(raio**3)

            exp1 = (parteExterna*(raio**2))/(diferenca)

            exp2 = (2*velSub*raio)/(diferenca)

            exp3 = (2*velDes*raio)/(diferenca)

            exp4 = (3*segundaParteInterna*soma)/(2*math.sqrt((primeiraParteInterna**2)+segundaParteInterna*diferenca))

            erroCarga = (abs(exp1*(exp4-exp2))*desvPadAmostMediaVelDes)+(abs(exp1*(exp3-exp4))*desvPadAmostMediaVelSub)

            erroRaio = (abs((segundaParteInterna)/(2*math.sqrt((primeiraParteInterna**2)+segundaParteInterna*diferenca)))*desvPadAmostMediaVelDes)+(abs((-segundaParteInterna)/(2*math.sqrt((primeiraParteInterna**2)+segundaParteInterna*diferenca)))*desvPadAmostMediaVelSub)

        # Todos os resultados são colocados em uma array, onde
        # por sua vez essa array é retornada e a depender do que
        # é necessitado, o índice é explicitado para garantir que 
        # vá vir só o resultado necessário do conjunto
        resultados.append(carga) # índice 0

        resultados.append(raio) # índice 1

        resultados.append(erroCarga) # índice 2

        resultados.append(erroRaio) # índice 3

        resultados.append(erroCarga/carga) # índice 4

        resultados.append(erroRaio/raio) # índice 5

        return resultados

    def prepararTabelaGraficoHistograma(self):

        self.atualizar_progresso(80, "Preparando para dispor os resultados em uma tabela")

        arrayGeralNomes = []

        arrayGeralQualidades = []

        arrayGeralCargas = []
        
        arrayGeralRaios = []

        """arrGeralErrRelCarga = []

        arrGeralErrRelRaio = []"""

        arrGeralErrCarga = []

        arrGeralErrRaio = []

        for i in range(len(self.arrayVoltagens)):

            arrayGeralNomes += self.arrArrsNomFileP_Voltgm[i]

            arrayGeralQualidades += self.arrArrsClassifGotP_Vltgm[i]

            arrayGeralCargas += self.arrArrsCargasP_Vltgm[i]
            
            arrayGeralRaios += self.arrArrsRaiosP_Vltgm[i]

            """arrGeralErrRelCarga += self.arrArrsPorctErrCargasP_Vltgm[i]"""

            """arrGeralErrRelRaio += self.arrArrsPorctErrRaiosP_Vltgm[i]"""

            arrGeralErrCarga += self.arrArrsErrCargasP_Vltgm[i]

            arrGeralErrRaio += self.arrArrsErrRaiosP_Vltgm[i]

        """baseParaDf = {
            "Nome da gota": arrayGeralNomes,
            "Qualidade da gota": arrayGeralQualidades,
            "Carga (C)": arrayGeralCargas,
            "Erro relativo (%) (C)": [x * 100 for x in arrGeralErrRelCarga],
            "Raio (m)": arrayGeralRaios,
            "Erro relativo (%) (m)": [x * 100 for x in arrGeralErrRelRaio]
        }"""

        baseParaDf = {
            "Nome da gota": arrayGeralNomes,
            "Qualidade da gota": arrayGeralQualidades,
            "Carga (C)": arrayGeralCargas,
            "Erro (·10\u207B\u00B9\u2079 C)": [x * 10**19 for x in arrGeralErrCarga],
            #"Erro (C)": [x * 100 for x in arrGeralErrRelCarga],
            "Raio (m)": arrayGeralRaios,
            #"Erro (m)": [x * 100 for x in arrGeralErrRelRaio]
            "Erro (m)": arrGeralErrRaio
        }

        self.dataFrameTabela = pd.DataFrame(baseParaDf)

        self.modelo = PandasModel(self.dataFrameTabela)

        self.tabela.setModel(self.modelo)

        self.modelo.layoutChanged.emit()       
        
        self.atualizar_progresso(90, "Preparando o gráfico para visualização")

        self.fig = Figure(figsize=(7,5))

        self.canvas = FigureCanvas(self.fig)

        """self.axGraf = self.canvas.figure.add_subplot(121)

        self.axHist = self.canvas.figure.add_subplot(122)"""

        self.toolbar = NavigationToolBar(self.canvas, self)

        self.atualizar_progresso(100, "Completo")   

        self.janela_execucao.hide()

        self.janela_avaliacao.show()

        self.janela_avaliacao.setWindowIcon(QIcon(resource_path(r'icones\logoAlternativa.ico')))

        self.janela_execucao.close()

        self.exibirGraficoCarga_RaioHistograma()

        if (len(self.arrayGotaNull) > 0):

            gotasImagem = ''

            for j1 in range(len(self.arrayGotaNull)):

                if j1 != (len(self.arrayGotaNull)-1):

                    gotasImagem += f'{self.arrayGotaNull[j1]},\n'

                else:

                    gotasImagem += f'{self.arrayGotaNull[j1]}'
    
            QMessageBox.warning(self,"Aviso",f"As gotas:\n{gotasImagem}\nforam excluídas da análise devido\nà discrepância de velocidade.\nSaiba mais sobre esses critérios no manual do\nsoftware.")

        if (len(self.arrayGotaNullPorVel) > 0):

            gotasVelocidade = ''

            for j2 in range(len(self.arrayGotaNullPorVel)):

                if j2 != (len(self.arrayGotaNullPorVel)-1):

                    gotasVelocidade += f'{self.arrayGotaNullPorVel[j2]},\n'

                else:

                    gotasVelocidade += f'{self.arrayGotaNullPorVel[j2]}'

            QMessageBox.warning(self,"Segundo aviso",f"As gotas:\n{gotasVelocidade}\nforam desconsideradas por insuficiência\nde pontos de velocidade\nSaiba mais sobre esses critérios no manual do\nsoftware.")

    def criarCheckBoxes(self, enderecoCheckBox, enderecoVoltagem):

        self.janelaAvaliacao.checkBox = QtWidgets.QCheckBox(self.janelaAvaliacao.scrollAreaCheckBoxes)

        self.janelaAvaliacao.checkBox.setObjectName(f'chechbox{enderecoCheckBox}Voltagem{enderecoVoltagem}')

        self.janelaAvaliacao.checkBox.setText(f'{self.arrArrsNomFileP_Voltgm[enderecoVoltagem][enderecoCheckBox]}')

        self.janelaAvaliacao.checkBox.stateChanged.connect(self.exibirGraficoCarga_RaioHistograma)

        self.janelaAvaliacao.gridLayout_11.addWidget(self.janelaAvaliacao.checkBox)

        return self.janelaAvaliacao.checkBox
    
    ########################
    ########################
    # MÉTODOS DE AVALIAÇÃO #
    ########################
    ########################

    # Método responsável pela exibição/
    # atualização do gráfico carga x raio
    def exibirGraficoCarga_RaioHistograma(self):

        cores = list(mcolors.TABLEAU_COLORS.keys())

        self.fig.clf()

        menorCarga = (self.dataFrameTabela.iloc[:,2].min())*10**(19)

        indiceMenorCarga = self.dataFrameTabela.iloc[:,2].idxmin()

        maiorCarga = (self.dataFrameTabela.iloc[:,2].max())*10**(19)

        indiceMaiorCarga = self.dataFrameTabela.iloc[:,2].idxmax()

        erroSuperiorMaiorCarga = self.dataFrameTabela.iloc[indiceMaiorCarga,3]

        erroInferiorMenorCarga = self.dataFrameTabela.iloc[indiceMenorCarga,3]

        """diferenca = maiorCarga - menorCarga

        numeroDeCompartimentos = round(diferenca/self.janelaAvaliacao.doubleSpinBoxLarguraCompartimento.value())"""

        gridspec = self.fig.add_gridspec(1,2, width_ratios=[3, 1], wspace=0.05)

        ax_grafico = self.fig.add_subplot(gridspec[0, 0])

        if self.checkBoxBarraErro.isChecked() == True:

            # Note que aqui utiliza a ideia
            # de retornar uma array. O elemento de 
            # endereço 0 retorna a array de cargas 
            # e o endereço 2 retorna a array de raios
            for i in range(len(self.arrayVoltagens)):
                
                ax_grafico.errorbar(self.alterarVisibilidadeGota(enderecoVoltagem=i)[2], self.alterarVisibilidadeGota(enderecoVoltagem=i)[0], xerr=self.alterarVisibilidadeGota(enderecoVoltagem=i)[3], yerr=self.alterarVisibilidadeGota(enderecoVoltagem=i)[1], label=f'{self.arrayVoltagens[i]} V', color=cores[i % len(cores)],fmt=".", markersize=5, capsize=5)

        else:

            for j in range(len(self.arrayVoltagens)):
                
                ax_grafico.scatter(self.alterarVisibilidadeGota(enderecoVoltagem=j)[2], self.alterarVisibilidadeGota(enderecoVoltagem=j)[0], label=f'{self.arrayVoltagens[j]} V', color=cores[j % len(cores)], marker=".", s=50)

        multiplos = self.aplicarMultiploCargaElementar(valCargElmnt=self.dSpinBoxCargElemnt.value())

        if multiplos is not None:

            for k in multiplos:

                ax_grafico.axhline(y=k, color="black", linestyle='-', linewidth=2.5)

        # Aumentando a grossura das bordas do gráfico
        ax_grafico.spines['top'].set_linewidth(2)
        ax_grafico.spines['bottom'].set_linewidth(2)
        ax_grafico.spines['left'].set_linewidth(2)
        ax_grafico.spines['right'].set_linewidth(2)

        # Aumentando a fonte dos números dos eixos
        ax_grafico.tick_params(axis='both', labelsize=14)

        # Colocando os títulos nos eixos
        ax_grafico.set_xlabel("Raio (m)", fontsize=14)

        ax_grafico.set_ylabel("Carga (C)", fontsize=14)

        ax_grafico.legend(fontsize=12)

        ax_grafico.set_ylim((menorCarga-erroInferiorMenorCarga-0.1)*10**(-19),(maiorCarga+erroSuperiorMaiorCarga+0.1)*10**(-19))

        ax_hist = self.fig.add_subplot(gridspec[0, 1])

        todasCargas = np.array([])

        for l in range(len(self.arrayVoltagens)):

            cargas = np.array(self.alterarVisibilidadeGota(enderecoVoltagem=l)[0])*10**19

            todasCargas = np.concatenate((todasCargas, cargas))

        ax_hist.hist(todasCargas, bins=round(self.janelaAvaliacao.doubleSpinBoxLarguraCompartimento.value()), orientation='horizontal', color='lightgray', edgecolor='black')

        ax_hist.set_yticks([])

        ax_hist.set_ylim((menorCarga-erroInferiorMenorCarga-0.1), (maiorCarga+erroSuperiorMaiorCarga+0.1))

        self.canvas.draw()

        if not hasattr(self, 'toolbar'):

            self.toolbar = NavigationToolBar(self.canvas, self)

        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.canvas)

    def alterarVisibilidadeGota(self, enderecoVoltagem):

        # Arrays temporárias para
        # carga, raio e seus erros
        arrayCargasTemp = []

        arrayCargasErrTemp = []

        arrayRaiosTemp = []

        arrayRaiosErrTemp = []

        arrayNomesTemp = []

        arrayQualidadesTemp = []

        resultados = [arrayCargasTemp, arrayCargasErrTemp, arrayRaiosTemp, arrayRaiosErrTemp, arrayNomesTemp, arrayQualidadesTemp]

        numeroDeRepeticoes = len(self.arrArrsCargasP_Vltgm[enderecoVoltagem])

        for i in range(numeroDeRepeticoes):

            # Se o checkBox (que tem o mesmo
            # endereço que o raio e carga
            # de certa gota) não está checkado,
            # o append dessas informações é pulado
            # e a array temporária só vai ter as
            # gotas que estão checkadas
            if self.arrArrsCheckBoxesP_Vltgm[enderecoVoltagem][i].isChecked() == True:

                continue

            arrayCargasTemp.append(self.arrArrsCargasP_Vltgm[enderecoVoltagem][i])

            arrayRaiosTemp.append(self.arrArrsRaiosP_Vltgm[enderecoVoltagem][i])

            arrayCargasErrTemp.append(self.arrArrsErrCargasP_Vltgm[enderecoVoltagem][i])

            arrayRaiosErrTemp.append(self.arrArrsErrRaiosP_Vltgm[enderecoVoltagem][i])

            arrayNomesTemp.append(self.arrArrsNomFileP_Voltgm[enderecoVoltagem][i])

            arrayQualidadesTemp.append(self.arrArrsClassifGotP_Vltgm[enderecoVoltagem][i])

        if self.janelaAvaliacao.checkBoxExcluiCargaPorErro.isChecked() == True:

            tamanhoTemporario = len(arrayCargasErrTemp)

            for j in range(tamanhoTemporario-1,-1,-1):

                if arrayCargasErrTemp[j] >= ((self.janelaAvaliacao.doubleSpinBoxErroLimite.value())*10**(-19)):

                    arrayCargasTemp.pop(j)

                    arrayCargasErrTemp.pop(j)

                    arrayRaiosTemp.pop(j)

                    arrayRaiosErrTemp.pop(j)

                    arrayQualidadesTemp.pop(j)

                    arrayNomesTemp.pop(j)

        # Essas arrays são requisitadas no plot em si
        return resultados
    
    def aplicarMultiploCargaElementar(self, valCargElmnt):

        valCargElmnt *= 10**(-19)
        # Determinando os mínimos e máximos globais de raio
        # e carga a partir do dataFrame geral

        menorCarga = self.dataFrameTabela.iloc[:,2].min()

        maiorCarga = self.dataFrameTabela.iloc[:,2].max()

        arrayMultplsCarg = []

        if self.janelaAvaliacao.checkBoxRetirarMultiplos.isChecked() == True:
        
            pass

        else:

            if menorCarga and maiorCarga is not None:

                for i in range(1,1001,1):

                    multiplovalCargElmnt = valCargElmnt * i
                    arrayMultplsCarg.append(multiplovalCargElmnt)

                arrayMultplsCarg = [item for item in arrayMultplsCarg if menorCarga <= item <= maiorCarga]

        if arrayMultplsCarg:

            return arrayMultplsCarg
        
        else:

            return None

    def escolherPastaSaveVelsGotas(self):

        nomePasta = None

        opcoes = QFileDialog.Options()

        nomePasta = QFileDialog.getExistingDirectory(
            self,
            "Escolha a pasta para salvar as planilhas de velocidades",
            "",
            options=opcoes
            )

        if nomePasta:

            self.salvarVelocidades(nomePasta)

        else:

            QMessageBox.information(
                self, 
                "Você não salvou os dados de velocidade", "Os dados de velocidade não foram salvos."
                )
            
    def salvarVelocidades(self, nomePasta):

        numPastasVltgns = len(self.arrayVoltagens)

        arrArrArrsDfsVels = []

        # Vamos adicionar as voltagens primeiro
        for i in range(numPastasVltgns):

            arrArrArrsDfsVels.append([])

            # E agora o número de gotas que tem nessa voltagem
            # Tanto faz se for arrArrArrsVelDesP_Vltgm ou 
            # arrArrArrsSubDesP_Vltgm
            numGotas = len(self.arrArrArrsVelDesP_Vltgm[i])
            
            for j in range(numGotas):

                arrArrArrsDfsVels[i].append([])

        # Agora em cada gota deve ser coletado os arrays
        # de velocidades e instantes
        for k in range(numPastasVltgns):
            
            numGotas = len(self.arrArrArrsVelDesP_Vltgm[k])

            for l in range(numGotas):

                dfSubida = None

                dfDescida = None

                dfNull = None

                # Começando pela velocidade de subida

                dadosSubida = {
                    "Velocidade de subida (m/s)": self.arrArrArrsVelSubP_Vltgm[k][l],
                    "Instante (s)": self.arrArrArrsVelSubP_VltgmInsts[k][l]
                }

                dfSubida = pd.DataFrame(dadosSubida)

                arrArrArrsDfsVels[k][l].append(dfSubida)

                dadosDescida = {
                    "Velocidade de descida (m/s)": self.arrArrArrsVelDesP_Vltgm[k][l],
                    "Instante (s)": self.arrArrArrsVelDesP_VltgmInsts[k][l]
                }

                dfDescida = pd.DataFrame(dadosDescida)

                arrArrArrsDfsVels[k][l].append(dfDescida)

                dadosNull = {
                    "Velocidade desconsiderada (m/s)": self.arrArrArrsVelP_VltgmNull[k][l],
                    "Instante (s)": self.arrArrArrsVelP_VltgmNullInsts[k][l]
                }

                dfNull = pd.DataFrame(dadosNull)

                arrArrArrsDfsVels[k][l].append(dfNull)

        caminhos = []

        for m in range(numPastasVltgns):

            subPastaVltgm = f"{self.arrayVoltagens[m]}"

            caminho = os.path.join("resultsVelocidades", subPastaVltgm)

            caminhos.append(caminho)

        for n in range(numPastasVltgns):

            CAMINHO = os.path.join(nomePasta, caminhos[n])

            os.makedirs(CAMINHO, exist_ok=True)

            # Restringe ao número de gotas como assim foi feito
            # anteriormente no laço de repetição j desse método
            for o in range(len(self.arrArrArrsVelDesP_Vltgm[n])):
                
                # Aqui eu adiciono o nome do arquivo .xlsx
                # Como os dados são organizados concomitantemente
                # os índices n e o valerão para
                # arrArrsNomFileP_Voltgm e o método corrigirSheetNames
                # vai preparar ele apropriadamente tirando caracteres inválidos
                # e adicionando a terminação .xlsx
                caminhoArquivo = os.path.join(CAMINHO, self.corrigirSheetNames(self.arrArrsNomFileP_Voltgm[n][o]))

                with pd.ExcelWriter(caminhoArquivo) as writer:
                    
                    # E agora a distinção por aba:
                    # Onde o nome da aba é padronizado
                    # seguindo a ordem 1) velsSub, 2)
                    # velsDes, 3) velsDesconsidrds
                    for p in range(3):

                        if p == 0:

                            nomeAba = 'velsSub'

                            arrArrArrsDfsVels[n][o][p].to_excel(writer, sheet_name=nomeAba, index=False)

                        elif p == 1:

                            nomeAba = 'velsDes'

                            arrArrArrsDfsVels[n][o][p].to_excel(writer, sheet_name=nomeAba, index=False)

                        else:

                            nomeAba = 'velsDesconsidrds'

                            arrArrArrsDfsVels[n][o][p].to_excel(writer, sheet_name=nomeAba, index=False)

    def escolherPastaSaveDadosGotas(self):

        nomeArquivo = None

        opcoes = QFileDialog.Options()

        filtroDeArquivo = "Excel Files (*.xlsx);;All Files (*)"

        nomeArquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Escolha a pasta para salvar a planilha de dados",
            "",
            filtroDeArquivo,
            options=opcoes
            )

        if nomeArquivo:

            if not nomeArquivo.endswith('.xlsx'):

                nomeArquivo += '.xlsx'

            self.salvarTabela(nomeArquivo)

        else:

            QMessageBox.information(
                self, 
                "Você não salvou a planilha de dados", "Os dados da tabela não foram salvos."
                )
            
    def desconsiderarDados(self, enderecoVoltagem):

        baseParaDf = {
            "Nome da gota": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[4],
            "Qualidade da gota": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[5],
            "Carga (C)": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[0],
            "Erro relativo (%) (C)": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[1],
            "Raio (m)": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[2],
            "Erro relativo (%) (m)": self.alterarVisibilidadeGota(enderecoVoltagem=enderecoVoltagem)[3]
        }

        self.arrDfP_Vltgm[enderecoVoltagem] = pd.DataFrame(baseParaDf)

        return self.arrDfP_Vltgm[enderecoVoltagem]
            
    def salvarTabela(self, nomeArquivo):

        numVltgns = len(self.arrayVoltagens)

        with pd.ExcelWriter(nomeArquivo) as writer2:

            for i in range(numVltgns):

                self.desconsiderarDados(enderecoVoltagem=i).to_excel(writer2, sheet_name=str(self.arrayVoltagens[i]), index=False)

    def escolherPastaSaveDadosHist(self):

        nomeArquivo = None

        opcoes = QFileDialog.Options()

        filtroDeArquivo = "Excel Files (*.xlsx);;All Files (*)"

        nomeArquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Escolha a pasta para salvar os dados do histograma",
            "",
            filtroDeArquivo,
            options=opcoes
            )

        if nomeArquivo:

            if not nomeArquivo.endswith('.xlsx'):

                nomeArquivo += '.xlsx'

            self.salvarDadosHistograma(nomeArquivo)

        else:

            QMessageBox.information(
                self, 
                "Você não salvou a planilha de dados", "Os dados do histograma não foram salvos."
                )

    def salvarDadosHistograma(self, nomeArquivoHist):

        """menorCarga = (self.dataFrameTabela.iloc[:,2].min())*10**(19)

        maiorCarga = (self.dataFrameTabela.iloc[:,2].max())*10**(19)

        diferenca = maiorCarga - menorCarga

        numeroDeCompartimentos = round(diferenca/self.janelaAvaliacao.doubleSpinBoxLarguraCompartimento.value())"""

        todasCargas = np.array([])

        todosErros = np.array([])

        for i in range(len(self.arrayVoltagens)):

            cargas = np.array(self.alterarVisibilidadeGota(enderecoVoltagem=i)[0])*10**19

            erros = np.array(self.alterarVisibilidadeGota(enderecoVoltagem=i)[1])*10**19

            todasCargas = np.concatenate((todasCargas, cargas))

            todosErros = np.concatenate((todosErros, erros))

        _, limites = np.histogram(todasCargas, bins=round(self.janelaAvaliacao.doubleSpinBoxLarguraCompartimento.value()))

        bin_idx = np.digitize(todasCargas, limites) - 1
        bin_idx = np.clip(bin_idx, 0, len(limites) - 2)

        colunas = {}

        for j in range(len(limites) - 1):

            mascara = bin_idx ==  j

            cargas_intervalo = todasCargas[mascara]
            erros_intervalo = todosErros[mascara]

            col_carga = f"Carga_{j+1}"
            col_erro = f"Erro_{j+1}"

            colunas[col_carga] = list(cargas_intervalo)
            colunas[col_erro] = list(erros_intervalo)

        max_len = max(len(v) for v in colunas.values())

        for k in colunas:

            colunas[k] += [np.nan] * (max_len - len(colunas[k]))

        dataFrameParaHistograma = pd.DataFrame(colunas)

        with pd.ExcelWriter(nomeArquivoHist) as writer3:

            dataFrameParaHistograma.to_excel(writer3, index=False)

    def corrigirSheetNames(self, nomePlanilha):
        
        # Array de caracteres inválidos
        chars_invalidos = ['\\', '/', '*', '[', ']', ':', '?', "'", '"', '<', '>', '|']
        
        # Laço de repetição analisando cada caractere do 
        # nomeSheet comparando com os caracteres inválidos
        for char in chars_invalidos:
            
            # Onde caso ocorra presença de algum caractere do   
            # tipo inválido deve haver reposição pelo caractere _
            nomePlanilha = nomePlanilha.replace(char, '_')
        
        # Verificando se o número de caracteres excede 31
        if len(nomePlanilha) > 31:
            
            # Se sim, restringir aos 31 caracteres
            nomePlanilha = nomePlanilha[:31]

        if not nomePlanilha.endswith('.xlsx'):

            nomePlanilha += '.xlsx'
        
        return nomePlanilha.strip()
    
    def reinicializar(self):

        self.janela_avaliacao.close()

        self.layout.removeWidget(self.canvas)

        self.canvas.setParent(None)

        self.layout.removeWidget(self.toolbar)

        self.toolbar.setParent(None)

        #############
        #############
        # ATRIBUTOS #
        #############
        #############

        # "Array 2D" que vai armazenar os caminhos de cada voltagem
        self.arrayArrayPaths = []

        # Array que vai armazenar as voltagens
        self.arrayVoltagens = []

        # Array 2D dos nomes dos arquivos por voltagem
        self.arrArrsNomFileP_Voltgm = []

        # Array das arrays de velocidades de subida e descida
        self.arrArrArrsVelSubP_Vltgm = []

        self.arrArrArrsVelDesP_Vltgm = []

        # Array das arrays de velocidades desconsideradas
        self.arrArrArrsVelP_VltgmNull = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades de subida e descida
        self.arrArrArrsVelSubP_VltgmInsts = []

        self.arrArrArrsVelDesP_VltgmInsts = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades desconsideradas
        self.arrArrArrsVelP_VltgmNullInsts = []

        # Array de desvios padrões amostrais das velocidades 
        # de subida e descida
        self.arrArrsDesvPadAmostVelSubP_Vltgm = []

        self.arrArrsDesvPadAmostVelDesP_Vltgm = []

        #Array de médias das velocidades de subida e descida
        self.arrArrsMedVelSubP_Vltgm = []

        self.arrArrsMedVelDesP_Vltgm = []

        # Array de desvios padrões amostrais da média de (erros) 
        # velocidades de subida e descida
        self.arrArrsDesvPadAmostMedVelDesP_Vltgm = []

        self.arrArrsDesvPadAmostMedVelSubP_Vltgm = []

        # Arrays das cargas, raios (E seus erros) 
        # das gotas (E por fim, os erros relativos)
        self.arrArrsCargasP_Vltgm = []

        self.arrArrsErrCargasP_Vltgm = []

        self.arrArrsPorctErrCargasP_Vltgm = []

        self.arrArrsRaiosP_Vltgm = []

        self.arrArrsErrRaiosP_Vltgm = []

        self.arrArrsPorctErrRaiosP_Vltgm = []

        # Array das classificações das gotas
        self.arrArrsClassifGotP_Vltgm = []

        # Importante limpar o layout de checkboxes. Caso
        # contrário, eles irão se acumular a cada cálculo
        # refeito
        self.limpar_layout(self.janelaAvaliacao.gridLayout_11)

        self.arrArrsCheckBoxesP_Vltgm.clear()

        # Array para as gotas desconsideradas no caso de imagem
        # invertida (O nome delas no caso)
        self.arrayGotaNull = []

        # Array para as gotas desconsideradas no caso de falta
        # de quantidade de pontos de velocidade suficiente para
        # cálculos estatísticos
        self.arrayGotaNullPorVel = []

        # Esse dado vai ser somente utilizado como
        # modelo para tabela
        self.dataFrameTabela = None

        # Essa array irá armazenar diferentes dataframes
        # por voltagem
        self.arrDfP_Vltgm = []

        # Inicialização do atributo diretório
        self.diretorio = None

        self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        # Inicialização do atributo densidade da gota
        self.densGot = None

        # Inicialização do atributo distância das placas
        self.distPlacs = None

        # Inicialização do atributo varredura
        self.varredura = 5

        # Inicialização da constante 1
        self.constante1 = None

        # Inicialização da constante 2
        self.constante2 = None

        # Valor da viscosidade do ar utilizado 
        self.viscosidadeAr = None

        # Valor da gravidade [m*s^-2]
        self.gravidade = 9.80665

        # Densidade do ar [Kg*m^-3]
        self.densidadeAr_p2 = None

        self.show()

    # Feito especialmente para o grid_layout11
    def limpar_layout(self, layout):
        
        # Enquanto ainda houver itens no grid_layout11
        while layout.count():
            
            item = layout.takeAt(0)  # remove o primeiro item
            
            widget = item.widget() # Descobre qual tipo de widget é
            
            # Caso ele não seja vazio ou um sub-layout
            if widget is not None:
                
                widget.setParent(None)  # remove do layout visualmente
                
                # Garante que ele será deletado no próximo
                # loop de eventos de forma segura
                widget.deleteLater()

            # Como eu sei que esse grid_layout não tem sub-
            # -layouts, não adicionei o tratamento para esse
            # tipo de widget

    #####################
    #####################
    # MÉTODOS DE EDIÇÃO #
    #####################
    #####################

    def abrirMenuContexto(self, position: QPoint):

        index = self.tabela.indexAt(position)

        if not index.isValid():

            return
        
        row = index.row()

        menu = QMenu(self)

        acaoAbrirDetalhes = menu.addAction("Ver a varredura de velocidades")

        action = menu.exec_(self.tabela.viewport().mapToGlobal(position))

        if action == acaoAbrirDetalhes:

            if 0 <= row < self.modelo._data.shape[0]:

                self.janela_detalhes.show()

                # Caso esteja minimizada ativamente,
                # esse comando garante que ele mude seu estado
                # para ativo antes de utilizar o raise_()
                self.janela_detalhes.setWindowState(
                    self.janela_detalhes.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
                )

                self.janela_detalhes.raise_()

                self.janela_detalhes.setWindowIcon(QIcon(resource_path(r'icones\logoAlternativa.ico')))

                indiceVoltagem = self.arrayVoltagens.index(int(self.dataFrameTabela.iloc[row,0][:3]))

                indiceGota = self.arrArrsNomFileP_Voltgm[indiceVoltagem].index(self.dataFrameTabela.iloc[row,0])

                arrVelsSubida = self.arrArrArrsVelSubP_Vltgm[indiceVoltagem][indiceGota]

                arrVelsSubidaInsts = self.arrArrArrsVelSubP_VltgmInsts[indiceVoltagem][indiceGota]

                arrVelsDescida = self.arrArrArrsVelDesP_Vltgm[indiceVoltagem][indiceGota]

                arrVelsDescidaInsts = self.arrArrArrsVelDesP_VltgmInsts[indiceVoltagem][indiceGota]

                arrVelNull = self.arrArrArrsVelP_VltgmNull[indiceVoltagem][indiceGota]
                
                arrVelNullInsts = self.arrArrArrsVelP_VltgmNullInsts[indiceVoltagem][indiceGota]

                unificacaoVel = []

                unificacaoVel += arrVelsSubida

                unificacaoVel += arrVelsDescida

                unificacaoVel += arrVelNull

                unificacaoInsts = []

                unificacaoInsts += arrVelsSubidaInsts

                unificacaoInsts += arrVelsDescidaInsts

                unificacaoInsts += arrVelNullInsts

                self.exibirGraficoVelocidades(arrVelNull=arrVelNull, arrVelNullInsts=arrVelNullInsts, arrVelsDescida=arrVelsDescida, arrVelsDescidaInsts=arrVelsDescidaInsts, arrVelsSubida=arrVelsSubida, arrVelsSubidaInsts=arrVelsSubidaInsts, unificacaoVel=unificacaoVel, unificacaoInsts=unificacaoInsts, row=row)

            else:

                raise ValueError(f"A linha {row} é inválida.")
            
    def exibirGraficoVelocidades(self, arrVelNull, arrVelNullInsts, arrVelsDescida, arrVelsDescidaInsts, arrVelsSubida, arrVelsSubidaInsts, unificacaoVel, unificacaoInsts, row):

        if hasattr(self, 'canvasDetalhes'):

            self.layoutDetalhes.removeWidget(self.canvasDetalhes)

            self.canvasDetalhes.setParent(None)

            del self.axDetalhes

            del self.canvasDetalhes

            self.canvasDetalhes = None

        if hasattr(self, 'toolbarDetalhes'):

            self.layoutDetalhes.removeWidget(self.toolbarDetalhes)

            self.toolbarDetalhes.setParent(None)

            del self.toolbarDetalhes

            self.toolbarDetalhes = None

        self.canvasDetalhes = FigureCanvas(Figure(figsize=(5,4)))

        self.axDetalhes = self.canvasDetalhes.figure.add_subplot(111)

        self.toolbarDetalhes = NavigationToolBar(self.canvasDetalhes, self)

        self.axDetalhes.scatter(arrVelsSubidaInsts, arrVelsSubida, color="red", marker='o', label='Velocidade de subida')

        self.axDetalhes.scatter(arrVelsDescidaInsts, arrVelsDescida, color="blue", marker='o', label='Velocidade de descida')

        self.axDetalhes.scatter(arrVelNullInsts, arrVelNull, color='gray', marker='o', label='Velocidade desconsiderada')

        self.axDetalhes.spines['top'].set_linewidth(2)

        self.axDetalhes.spines['bottom'].set_linewidth(2)

        self.axDetalhes.spines['left'].set_linewidth(2)

        self.axDetalhes.spines['right'].set_linewidth(2)

        self.axDetalhes.tick_params(axis='both', labelsize=14)

        self.axDetalhes.set_xlabel('Instante (s)', fontsize=14)

        self.axDetalhes.set_ylabel('Velocidade vertical (m/s)', fontsize=14)

        self.axDetalhes.set_title(f'Varredura de velocidades da gota {self.dataFrameTabela.iloc[row,0]}')

        self.axDetalhes.legend(fontsize=12)

        self.canvasDetalhes.draw()

        self.layoutDetalhes.addWidget(self.toolbarDetalhes)

        self.layoutDetalhes.addWidget(self.canvasDetalhes)

    #####################
    #####################
    # MÉTODOS POPULARES # -> São utilizados por
    #####################    mais de uma janela
    #####################

    # Classificar as velocidades de dada gota i
    def classificarVelocidades(self, dataFrameVelocidades, enderecoGota, enderecoVoltagem):

        i = enderecoGota

        # Retorna o número de linhas
        quantidadeLinhas = dataFrameVelocidades.shape[0]

        def atribuicaoVelocidadeDescida():

            self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][i].append(velocidade)
            
            self.arrArrArrsVelDesP_VltgmInsts[enderecoVoltagem][i].append(instante)

        def atribuicaoVelocidadeSubida():

            self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][i].append(velocidade)
        
            self.arrArrArrsVelSubP_VltgmInsts[enderecoVoltagem][i].append(instante)

        def atribuirVelocidadeDesconsiderada():

            self.arrArrArrsVelP_VltgmNull[enderecoVoltagem][i].append(velocidade)
            
            self.arrArrArrsVelP_VltgmNullInsts[enderecoVoltagem][i].append(instante)

        for j in range(quantidadeLinhas):

            velocidade = dataFrameVelocidades.iloc[j,1]

            instante = dataFrameVelocidades.iloc[j,0]

            # Primeiro, vamos descobrir se o ponto analisado 
            # vai estar em um dos extremos ou no meio
            if j == 0:
                
                Pontuacao = self.varrerDianteira(dataFrameVelocidades, quantidadeLinhas, j)

                if Pontuacao > 0:

                    atribuicaoVelocidadeSubida()

                elif Pontuacao < 0:

                    atribuicaoVelocidadeDescida()

                elif Pontuacao == 0:

                    atribuirVelocidadeDesconsiderada()

            elif j != 0 and j != (quantidadeLinhas-1):

                PontuacaO = self.varrerDianteira(dataFrameVelocidades, quantidadeLinhas, j) + self.varrerTraseira(dataFrameVelocidades, j)

                if PontuacaO > 0:

                    atribuicaoVelocidadeSubida()

                elif PontuacaO < 0:

                    atribuicaoVelocidadeDescida()

                elif PontuacaO == 0:

                    atribuirVelocidadeDesconsiderada()

            elif j == (quantidadeLinhas-1):

                pontuacaO = self.varrerTraseira(dataFrameVelocidades, j)

                if pontuacaO > 0:

                    atribuicaoVelocidadeSubida()

                elif pontuacaO < 0:

                    atribuicaoVelocidadeDescida()

                elif pontuacaO == 0:

                    atribuirVelocidadeDesconsiderada()

    # Método direcionado para varredura do
    # que está a sua frente, utiliza o varredor
    # como ferramenta para varrer                
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

    # Método direcionado para varredura do
    # que está na sua retarguada, utiliza o varredor
    # como ferramenta para varrer
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

    # Método de varredura das velocidades 
    # que é utilizado pelos métodos anteriores
    # que por sua vez são utilizados pelo
    # método de classificação das velocidades
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
    
    # Método de classificação de dada gota i
    def classificarGota(self, enderecoGota, enderecoVoltagem):

        # Se um dos conjuntos de velocidade tiver
        # menos que 10 itens, é uma gota duvidosa
        if len(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][enderecoGota]) < 10 or len(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][enderecoGota]) < 10:

            return "Duvidoso"
        
        # Caso um dos conjuntos de velocidade tiver
        # entre 10 e 20 itens, é uma gota razoável
        elif (10 <= len(self.arrArrArrsVelDesP_Vltgm[enderecoVoltagem][enderecoGota]) <= 20) or (10 <= len(self.arrArrArrsVelSubP_Vltgm[enderecoVoltagem][enderecoGota]) <= 20):

            return "Razoável"

        # E caso os dois conjuntos tenham mais
        # de 20 itens, é uma gota confiável
        else:

            return "Confiável"

if __name__ == "__main__":

    # O erro do sistema vai ser direcionado ao método global
    sys.excepthook=capturarExcecao

    # Tente
    try:

        app = QApplication(sys.argv)

        window = MainWindow()

        window.show()

        sys.exit(app.exec_())
        
    # Exceto se
    except Exception as e:

        # Utiliza o método global para mostrar o erro no código
        capturarExcecao(*sys.exc_info())