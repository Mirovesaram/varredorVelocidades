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

from PyQt5 import QtWidgets

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
    erro.setWindowIcon(QIcon(resource_path(r'icones\logoMillikan.ico')))
    
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
        self.setWindowIcon(QIcon(resource_path(r"icones\logoMillikan.ico")))

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

        self.checkBoxBarraErro.stateChanged.connect(self.exibirGraficoCarga_Raio)

        self.tabela = self.janelaAvaliacao.tabelaGotas

        self.tabela.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tabela.customContextMenuRequested.connect(self.abrirMenuContexto)

        self.dSpinBoxCargElemnt = self.janelaAvaliacao.doubleSpinBoxCargElement

        self.dSpinBoxCargElemnt.valueChanged.connect(self.exibirGraficoCarga_Raio)

        self.pushButtonSalvarVels = self.janelaAvaliacao.pushButtonBaixarVels

        self.pushButtonSalvarVels.clicked.connect(self.escolherPastaSaveVelsGotas)

        self.pushButtonSalvarDados = self.janelaAvaliacao.pushButtonBaixarDf

        self.pushButtonSalvarDados.clicked.connect(self.escolherPastaSaveDadosGotas)

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

        # Array para as gotas desconsideradas (O nome delas no caso)
        self.arrayGotaNull = []

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
        # no manual da Phywe [kg*(m*s)^-1]
        self.viscosidadeAr = 1.82 * 10**(-5)

        # Valor da gravidade [m*s^-2]
        self.gravidade = 9.80665

        # Densidade do ar [Kg*m^-3]
        self.densidadeAr_p2 = 1.293

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
            
            self.prepararTabelaGrafico()

        else:
            
            QMessageBox.warning(self, "Erro", "A pasta que você escolheu não tem nenhum arquivo .txt")

    # Método para verificar se tudo foi devidamente 
    # preenchido e então extrair as variáveis para
    # executar os cálculos

    def extrairVariaveis(self):
            
        densGot = self.doubleSpinBoxDensGot.value()

        distPlacs = self.doubleSpinBox_distPlacs.value()

        #voltagem = self.doubleSpinBox_voltagem.value()

        #if densGot != 0 and voltagem != 0 and distPlacs != 0:

        if densGot != 0 and distPlacs != 0:#
    
            if self.diretorio:

                #self.voltagem = voltagem

                self.densGot = densGot

                self.distPlacs = distPlacs

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

        self.janela_execucao.setWindowIcon(QIcon(resource_path(r"icones\logoMillikan.ico")))

        # Fecha a anterior
        self.close()
    
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
                 
                 # Caso um erro seja encontrado, excluir tudo
                 # e "inicializar" novamente
                 self.cancelarOsCalculosFeitos()

                 raise ValueError(f"O dataframe do arquivo {txtEmAnalise} apresenta problemas")

            # dropna é uma função que exclui linhas onde há dados
            # ausentes (NaN)
            dataFrameVelocidades = dataFrameVelocidades.dropna()

            # Para fins de teste

            #print(dataFrameVelocidades.dtypes)  
            #print(dataFrameVelocidades.head())

            self.classificarVelocidades(dataFrameVelocidades=dataFrameVelocidades, enderecoGota=(i-1), enderecoVoltagem=enderecoVoltagem)

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

        self.atualizar_progresso(40, f"Calculando os valores de carga e raio das gotas e seus erros para {self.arrayVoltagens[enderecoVoltagem]}V")   

        # Calculando as cargas, os raios e seus erros
        for j in range(0,numeroDeRepeticoes-1,1):

            resultado = self.calcularCargaRaioGota(enderecoVoltagem=enderecoVoltagem, enderecoGota=j)

            if resultado is not None:

                # É necessário fazer dessa maneira pois colocar o .append no próprio
                # método de cálculos do raio e carga é problemático.
                self.arrArrsCargasP_Vltgm[enderecoVoltagem].append(resultado[0])

                self.arrArrsRaiosP_Vltgm[enderecoVoltagem].append(resultado[1])

                self.arrArrsErrCargasP_Vltgm[enderecoVoltagem].append(resultado[2])

                self.arrArrsErrRaiosP_Vltgm[enderecoVoltagem].append(resultado[3])

                self.arrArrsPorctErrCargasP_Vltgm[enderecoVoltagem].append(resultado[4])

                self.arrArrsPorctErrRaiosP_Vltgm[enderecoVoltagem].append(resultado[5])

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

        for k in range(numeroDeRepeticoes-1):

            self.arrArrsClassifGotP_Vltgm[enderecoVoltagem].append(self.classificarGota(enderecoGota=k, enderecoVoltagem=enderecoVoltagem))

        self.atualizar_progresso(60, f"Criando e configurando os check-boxes para {self.arrayVoltagens[enderecoVoltagem]}V")

        for l in range(numeroDeRepeticoes-1):

            self.arrArrsCheckBoxesP_Vltgm[enderecoVoltagem].append(self.criarCheckBoxes(enderecoCheckBox=l, enderecoVoltagem=enderecoVoltagem))

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

        carga = 2*razao*soma*math.sqrt(diferenca)

        erroCarga = (abs(primeiraParte+segundaParte)*desvPadAmostMediaVelDes)+(abs(primeiraParte-segundaParte)*desvPadAmostMediaVelSub)

        raio = constante2*math.sqrt(diferenca)

        parteAbs = (constante2)/(2*math.sqrt(diferenca))

        erroRaio = (abs(parteAbs)*desvPadAmostMediaVelDes)+(abs(-parteAbs)*desvPadAmostMediaVelSub)

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

    def prepararTabelaGrafico(self):

        self.atualizar_progresso(80, "Preparando para dispor os resultados em uma tabela")

        arrayGeralNomes = []

        arrayGeralQualidades = []

        arrayGeralCargas = []
        
        arrayGeralRaios = []

        arrGeralErrRelCarga = []

        arrGeralErrRelRaio = []

        for i in range(len(self.arrayVoltagens)):

            arrayGeralNomes += self.arrArrsNomFileP_Voltgm[i]

            arrayGeralQualidades += self.arrArrsClassifGotP_Vltgm[i]

            arrayGeralCargas += self.arrArrsCargasP_Vltgm[i]
            
            arrayGeralRaios += self.arrArrsRaiosP_Vltgm[i]

            arrGeralErrRelCarga += self.arrArrsPorctErrCargasP_Vltgm[i]

            arrGeralErrRelRaio += self.arrArrsPorctErrRaiosP_Vltgm[i]

        baseParaDf = {
            "Nome da gota": arrayGeralNomes,
            "Qualidade da gota": arrayGeralQualidades,
            "Carga (C)": arrayGeralCargas,
            "Erro relativo (%) (C)": [x * 100 for x in arrGeralErrRelCarga],
            "Raio (m)": arrayGeralRaios,
            "Erro relativo (%) (m)": [x * 100 for x in arrGeralErrRelRaio]
        }

        self.dataFrameTabela = pd.DataFrame(baseParaDf)

        self.modelo = PandasModel(self.dataFrameTabela)

        self.tabela.setModel(self.modelo)

        self.modelo.layoutChanged.emit()       
        
        self.atualizar_progresso(90, "Preparando o gráfico para visualização")  

        self.canvas = FigureCanvas(Figure(figsize=(5,4)))

        self.ax = self.canvas.figure.add_subplot(111)

        self.toolbar = NavigationToolBar(self.canvas, self)

        self.atualizar_progresso(100, "Completo")   

        self.janela_execucao.hide()

        self.janela_avaliacao.show()

        self.janela_avaliacao.setWindowIcon(QIcon(resource_path(r'icones\logoMillikan.ico')))

        self.janela_execucao.close()

        self.exibirGraficoCarga_Raio()

        if len(self.arrayGotaNull) > 0:

            gotas = ''

            for j in range(len(self.arrayGotaNull)):

                gotas += f'{self.arrayGotaNull[j]},\n'

                if j == (len(self.arrayGotaNull)-1):

                    gotas += f'{self.arrayGotaNull[j]}'

            QMessageBox.warning(self,"Aviso",f"As gotas:\n{gotas}\nforam excluídas da análise devido\nao critério de desclassificação.\n Saiba mais esse critério no manual do\nsoftware.")

    def criarCheckBoxes(self, enderecoCheckBox, enderecoVoltagem):

        self.janelaAvaliacao.checkBox = QtWidgets.QCheckBox(self.janelaAvaliacao.scrollAreaCheckBoxes)

        self.janelaAvaliacao.checkBox.setObjectName(f'chechbox{enderecoCheckBox}Voltagem{enderecoVoltagem}')

        self.janelaAvaliacao.checkBox.setText(f'{self.arrArrsNomFileP_Voltgm[enderecoVoltagem][enderecoCheckBox]}')

        self.janelaAvaliacao.checkBox.stateChanged.connect(self.exibirGraficoCarga_Raio)

        self.janelaAvaliacao.gridLayout_11.addWidget(self.janelaAvaliacao.checkBox)

        return self.janelaAvaliacao.checkBox
    
    ########################
    ########################
    # MÉTODOS DE AVALIAÇÃO #
    ########################
    ########################

    # Método responsável pela exibição/
    # atualização do gráfico carga x raio
    def exibirGraficoCarga_Raio(self):

        cores = list(mcolors.BASE_COLORS.keys())

        cores = [cor for cor in cores if cor not in ['k']]

        if hasattr(self, 'canvas'):

            pass

        else:

            self.canvas = FigureCanvas(Figure(figsize=(5,4)))
            self.ax = self.canvas.figure.add_subplot(111)

        if hasattr(self, 'ax'):

            self.ax.clear()

        else:

            self.canvas = FigureCanvas(Figure(figsize=(5,4)))
            self.ax = self.canvas.figure.add_subplot(111)

        if self.checkBoxBarraErro.isChecked() == True:

            # Note que aqui utiliza a ideia
            # de retornar uma array. O elemento de 
            # endereço 0 retorna a array de cargas 
            # e o endereço 2 retorna a array de raios
            for i in range(len(self.arrayVoltagens)):
                
                self.ax.errorbar(self.alterarVisibilidadeGota(enderecoVoltagem=i)[2], self.alterarVisibilidadeGota(enderecoVoltagem=i)[0], xerr=self.alterarVisibilidadeGota(enderecoVoltagem=i)[3], yerr=self.alterarVisibilidadeGota(enderecoVoltagem=i)[1], label=f'{self.arrayVoltagens[i]} V', color=cores[i % len(cores)],fmt="x", markersize=10, capsize=5)

        else:

            for j in range(len(self.arrayVoltagens)):
                
                self.ax.scatter(self.alterarVisibilidadeGota(enderecoVoltagem=j)[2], self.alterarVisibilidadeGota(enderecoVoltagem=j)[0], label=f'{self.arrayVoltagens[j]} V', color=cores[j % len(cores)], marker="x", s=100)

        for k in self.aplicarMultiploCargaElementar(valCargElmnt=self.dSpinBoxCargElemnt.value()):

            self.ax.axhline(y=k, color="black", linestyle='-', linewidth=2.5)

        # Aumentando a grossura das bordas do gráfico
        self.ax.spines['top'].set_linewidth(2)
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.spines['right'].set_linewidth(2)

        # Aumentando a fonte dos números dos eixos
        self.ax.tick_params(axis='both', labelsize=14)

        # Colocando os títulos nos eixos
        self.ax.set_xlabel("Raio (m)", fontsize=14)

        self.ax.set_ylabel("Carga (C)", fontsize=14)

        self.ax.legend(fontsize=12)

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

        resultados = [arrayCargasTemp, arrayCargasErrTemp, arrayRaiosTemp, arrayRaiosErrTemp]

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

        # Essas arrays são requisitadas no plot em si
        return resultados
    
    def aplicarMultiploCargaElementar(self, valCargElmnt):

        valCargElmnt *= 10**(-19)
        # Determinando os mínimos e máximos globais de raio
        # e carga a partir do dataFrame geral
        menorCarga = self.dataFrameTabela.iloc[:,2].min()

        maiorCarga = self.dataFrameTabela.iloc[:,2].max()

        arrayMultplsCarg = []

        for i in range(1,1001,1):

            multiplovalCargElmnt = valCargElmnt * i
            arrayMultplsCarg.append(multiplovalCargElmnt)

        arrayMultplsCarg = [item for item in arrayMultplsCarg if menorCarga <= item <= maiorCarga]

        return arrayMultplsCarg

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
            
    def salvarTabela(self, nomeArquivo):

        numVltgns = len(self.arrayVoltagens)

        with pd.ExcelWriter(nomeArquivo) as writer2:

            for i in range(numVltgns):

                self.arrDfP_Vltgm[i].to_excel(writer2, sheet_name=str(self.arrayVoltagens[i]), index=False)

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

                self.janela_detalhes.setWindowIcon(QIcon(resource_path(r'icones\logoMillikan.ico')))

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