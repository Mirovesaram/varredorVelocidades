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

import numpy as np

import glob

import time

import math

from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QFileDialog, QMessageBox, QCheckBox, QHBoxLayout, QVBoxLayout, QWidget

from PyQt5 import QtWidgets

from PyQt5.QtCore import QAbstractTableModel, Qt

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
        self.janela_edicao = QMainWindow()

        self.janelaEdicao = Ui_MainWindowJanelaDetalhes()

        self.janelaEdicao.setupUi(self.janela_edicao)

        # Estabelecimento de objetos já pré-existentes
        self.progressBar = self.janelaExecucao.progressBarExecucao

        self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        self.layout = self.janelaAvaliacao.gridLayout_Grafico

        self.tabela = self.janelaAvaliacao.tabelaGotas

        """
            Lembrar que aqui eu devo no futuro colocar
            os meios para permitir interagir com a tabela
        """

        ############
        ############
        # GATILHOS #
        ############
        ############

        self.pushButtonSelecPasta.clicked.connect(self.buscarDirArquivosTxt)

        self.pushButton_executar.clicked.connect(self.extrairVariaveis)

        self.janelaExecucao.pushButtonCancelar.clicked.connect(self.cancelarOsCalculosFeitos)

        #############
        #############
        # ATRIBUTOS #
        #############
        #############

        # "Array 2D" que vai armazenar os caminhos de cada voltagem
        self.arrayArrayPaths = []

        # Array que vai armazenar as voltagens
        self.arrayVoltagens = []

        """
        Aqui, podemos trabalhar da seguinte maneira, os endereços das arrays de voltagem podem
        coincidir com os endereços das arrays de arrays ("Arrays 2D") ou das "arrays 3D"
        Já adicionei o sistema de preenchimento da array 2d arrArrsNomFileP_Voltgm e a limpeza
        dela em caso de erro. Depois precisamos partir para as adequações do método executarCalculos
        """

        # Array 2D dos nomes dos arquivos por voltagem
        self.arrArrsNomFileP_Voltgm = []

        # Array das arrays de velocidades de subida e descida
        self.arrayDasArraysVelSub = []

        self.arrayDasArraysVelDes = []

        # Array das arrays de velocidades desconsideradas
        # que vão ser avaliadas pelo usuário
        self.arrayDasArraysVelDesconsdrds = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades de subida e descida
        self.arrayDasArraysVelSubInstantes = []

        self.arrayDasArraysVelDesInstantes = []

        # Array das arrays dos instantes correspondentes 
        # a essas velocidades desconsideradas
        # que vão ser avaliadas pelo usuário
        self.arrayDasArraysVelDesconsInsts = []

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

        # Arrays das cargas, raios (E seus erros) 
        # das gotas (E por fim, os erros relativos)

        self.arrayCargas = []

        self.arrayErrCargas = []

        self.arrayPorctErrCargas = []

        self.arrayRaios = []

        self.arrayErrRaios = []

        self.arrayPorctErrRaios = []

        # Array das classificações das gotas

        self.arrayClassificacoesGota = []

        # Array da estrutura dos checkboxes para considerar as gotas

        self.arrayCheckBoxes = []

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

            # Para fins de teste

            #print(self.diretorio)
        
        else:

            self.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")
            
            # Para fins de teste

            #print(self.diretorio)

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

                # Adiciona a voltagem como forma de validação
                # assim como foi feito anteriormente
                self.arrArrsNomFileP_Voltgm[i].append(voltagem)

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

                    self.arrArrsNomFileP_Voltgm[qtdVoltgs].append(nomesArquivosTxtOrden[i])

        self.arrayVoltagens = arrayVoltagens

    def lerDiretorio(self, diretorio):

        arrayCaminhosTxt = []

        self.diretorio = diretorio

        extensaoArquivo = '*.txt'

        buscaDosTxts = os.path.join(self.diretorio, extensaoArquivo)

        arrayCaminhosTxt = glob.glob(buscaDosTxts)

        """
        Pronto. Agora temos um arranjo que separa os caminhos por voltagem.
        Vamos avaliar como adicionar isso com certas modificações. Aproveitando
        um módulo responsivo. Vamos avaliar como reestruturar os métodos existentes 
        e as estruturas de dados já existentes.
        """

        if arrayCaminhosTxt != []:

            self.separarCaminhos(arrayCaminhosTxt)

            self.executarCalculos(arrayCaminhosTxt)

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
        self.progressBar.setValue(valor)

        # Altera o texto que acompanha
        self.progressBar.setFormat(f"{mensagem} ({valor}%)")

        # Comando para atualização da UI em tempo real, 
        # sem ser feito somente ao fim
        QApplication.processEvents()

    # O objetivo desse método é estabelecer os conjuntos iniciais,
    # ele só será para estabelecimento inicial dos resultados e outros
    # métodos se encarregarão de editar esses dados inicialmente 
    # estabelecidos aqui
    def executarCalculos(self, arrayCaminhosTxt):

        # Processo para transicionar entre janelas

        # Esconde a anterior
        self.hide()
        
        # Mostra a próxima
        self.janela_execucao.show()

        self.janela_execucao.setWindowIcon(QIcon(resource_path(r"icones\logoMillikan.ico")))

        # Fecha a anterior
        self.close()
        
        # Delays de 1s propositais
        time.sleep(0.5)
        
        self.atualizar_progresso(0, "Iniciando processamento")
        
        time.sleep(0.5)

        # Vou fazer uma iteração global do algoritmo que é
        # regida pelo número de arquivos txt presentes na pasta.
        numeroDeRepeticoes = len(arrayCaminhosTxt)

        time.sleep(0.5)
        
        self.atualizar_progresso(10, "Iniciando Varredura")
        
        time.sleep(0.5)

        # Configuração das constantes
        self.constante1 = (9/2)*(math.pi)*(self.distPlacs)*math.sqrt((self.viscosidadeAr**3)/(self.gravidade*(self.densGot-self.densidadeAr_p2)))

        self.constante2 = (3/2)*math.sqrt((self.viscosidadeAr)/(self.gravidade*(self.densGot-self.densidadeAr_p2)))

        time.sleep(0.5)
        
        self.atualizar_progresso(15, "Iniciando Varredura")
        
        time.sleep(0.5)

        # Definição padrão do alcance de varredura
        self.varredura = 5

        for i in range(numeroDeRepeticoes):

            # Estabelecimento das arrays

            self.arrayDasArraysVelSub.append([])

            self.arrayDasArraysVelDes.append([])

            self.arrayDasArraysVelDesconsdrds.append([])

            self.arrayDasArraysVelSubInstantes.append([])

            self.arrayDasArraysVelDesInstantes.append([])

            self.arrayDasArraysVelDesconsInsts.append([])

            txtEmAnalise = arrayCaminhosTxt[i]

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

            self.classificarVelocidades(dataFrameVelocidades, i)

            # Configuração inicial dos resultados 
            # para os conjuntos de velocidade, suas médias, 
            # seus desvios padrão amostrais e seus erros
            desvioPadraoAmostralVelocidadeDescida = np.std(self.arrayDasArraysVelDes[i], ddof=1)

            desvioPadraoAmostralVelocidadeSubida = np.std(self.arrayDasArraysVelSub[i], ddof=1)

            self.arrayDesvPadAmostVelSub.append(desvioPadraoAmostralVelocidadeSubida)

            self.arrayDesvPadAmostVelDes.append(desvioPadraoAmostralVelocidadeDescida)

            self.arrayMediaVelSub.append(np.mean(self.arrayDasArraysVelSub[i]))

            self.arrayMediaVelDes.append(np.mean(self.arrayDasArraysVelDes[i]))

            self.arrayDesvPadAmostMediaVelDes.append(desvioPadraoAmostralVelocidadeDescida/(math.sqrt(len(self.arrayDasArraysVelDes[i]))))

            self.arrayDesvPadAmostMediaVelSub.append(desvioPadraoAmostralVelocidadeSubida/(math.sqrt(len(self.arrayDasArraysVelSub[i]))))

            self.arrayCaminhosArquivos.append(arrayCaminhosTxt[i])

        time.sleep(0.5)

        self.atualizar_progresso(50, "Calculando os valores de carga e raio das gotas e seus erros")

        time.sleep(0.5)

        # Calculando as cargas, os raios e seus erros
        for i in range(numeroDeRepeticoes):

            # É necessário fazer dessa maneira pois colocar o .append no próprio
            # método de cálculos do raio e carga é problemático. Já que esse método
            # não vai ser utilizado só pelo método principal da janela de execução
            self.arrayCargas.append(self.calcularCargaRaioGota(i)[0])

            self.arrayRaios.append(self.calcularCargaRaioGota(i)[1])

            self.arrayErrCargas.append(self.calcularCargaRaioGota(i)[2])

            self.arrayErrRaios.append(self.calcularCargaRaioGota(i)[3])

            self.arrayPorctErrCargas.append(self.calcularCargaRaioGota(i)[4])

            self.arrayPorctErrRaios.append(self.calcularCargaRaioGota(i)[5])

        time.sleep(0.5)

        self.atualizar_progresso(60, "Classificando as gotas")

        time.sleep(0.5)

        for i in range(numeroDeRepeticoes):

            self.arrayClassificacoesGota.append(self.classificarGota(i))

        time.sleep(0.5)

        self.atualizar_progresso(70, "Nomeando os resultados a partir dos nomes de seus arquivos")

        time.sleep(0.5)

        # Essa linha de comando é colocada após o laço de repetição a fim de 
        # garantir que todos os nomes guardados são provenientes de resultados 
        # sem problemas na estrutura do arquivo .txt

        # splitext é para excluir a extensão .txt do fim do nome base (basename)
        self.arrayNomesArquivos = [os.path.splitext(os.path.basename(itemDoCaminhosTxt))[0] for itemDoCaminhosTxt in arrayCaminhosTxt]

        time.sleep(0.5)

        self.atualizar_progresso(80, "Preparando para dispor os resultados em uma tabela")

        time.sleep(0.5)

        for i in range(numeroDeRepeticoes):

            self.arrayCheckBoxes.append(self.criarCheckBoxes(i))

        baseParaDf = {
            "Nome da gota": self.arrayNomesArquivos,
            "Qualidade da gota": self.arrayClassificacoesGota,
            "Carga (C)": self.arrayCargas,
            "Erro relativo (%) (C)": [x * 100 for x in self.arrayPorctErrCargas],
            "Raio (m)": self.arrayRaios,
            "Erro relativo (%) (m)": [x * 100 for x in self.arrayPorctErrRaios]
        }

        self.dataFrameTabela = pd.DataFrame(baseParaDf)

        self.modelo = PandasModel(self.dataFrameTabela)

        self.tabela.setModel(self.modelo)

        self.modelo.layoutChanged.emit()

        time.sleep(0.5)
        
        self.atualizar_progresso(90, "Preparando o gráfico para visualização")
        
        time.sleep(0.5)

        self.canvas = FigureCanvas(Figure(figsize=(5,4)))

        self.ax = self.canvas.figure.add_subplot(111)

        self.toolbar = NavigationToolBar(self.canvas, self)

        time.sleep(0.5)
        
        self.atualizar_progresso(100, "Completo")
        
        time.sleep(0.5)

        # Para fins de teste
        """print(self.arrayErrCargas)
        print(self.arrayErrRaios)"""

        self.janela_execucao.hide()

        self.janela_avaliacao.show()

        self.janela_avaliacao.setWindowIcon(QIcon(resource_path(r'icones\logoMillikan.ico')))

        self.janela_execucao.close()

        self.exibirGraficoCarga_Raio()

    # Método de reincinialização do programa
    # antes da finalização dos cálculos iniciais
    def cancelarOsCalculosFeitos(self):

        # Precisa limpar as arrays e abrir novamente 
        # a janela principal fechando a de executar 
        # voltando ao estado inicial
        self.arrayDasArraysVelSub = []

        self.arrayDasArraysVelDes = []

        self.arrayDasArraysVelDesconsdrds = []

        self.arrayDasArraysVelSubInstantes = []

        self.arrayDasArraysVelDesInstantes = []

        self.arrayDasArraysVelDesconsInsts = []

        self.arrayDesvPadAmostVelSub = []

        self.arrayDesvPadAmostVelDes = []

        self.arrayMediaVelSub = []

        self.arrayMediaVelDes = []

        self.arrayDesvPadAmostMediaVelDes = []

        self.arrayDesvPadAmostMediaVelSub = []

        self.arrayCargas = []

        self.arrayErrCargas = []

        self.arrayPorctErrCargas = []

        self.arrayRaios = []

        self.arrayErrRaios = []

        self.arrayPorctErrRaios = []

        self.arrayClassificacoesGota = []

        self.arrayCheckBoxes = []

        self.diretorio = None

        self.voltagem = None

        self.densGot = None

        self.distPlacs = None

        self.varredura = 5

        self.constante1 = None

        self.constante2 = None

        self.viscosidadeAr = 1.82 * 10**(-5)

        self.gravidade = 9.80665

        self.densidadeAr_p2 = 1.293

        self.janelaAtribuicao.textEditCaminhoPasta.setText("O caminho da pasta aparecerá aqui quando selecionada")

        self.janela_execucao.hide()

        self.janela_atribuicao.show()

        self.janela_atribuicao.setWindowIcon(QIcon(resource_path(r"icones/logoMillikan.ico")))

        self.janela_execucao.close()

    def criarCheckBoxes(self, enderecoCheckBox):

        i = enderecoCheckBox

        self.janelaAvaliacao.checkBox = QtWidgets.QCheckBox(self.janelaAvaliacao.scrollAreaCheckBoxes)

        self.janelaAvaliacao.checkBox.setObjectName(f'chechbox{i}')

        self.janelaAvaliacao.checkBox.setText(f'{self.arrayNomesArquivos[i]}')

        self.janelaAvaliacao.checkBox.stateChanged.connect(self.exibirGraficoCarga_Raio)

        self.janelaAvaliacao.gridLayout_11.addWidget(self.janelaAvaliacao.checkBox)

        return self.janelaAvaliacao.checkBox
    
    ########################
    ########################
    # MÉTODOS DE AVALIAÇÃO #
    ########################
    ########################

    def alterarVisibilidadeGota(self):

        # Arrays temporárias para
        # carga, raio e seus erros
        arrayCargasTemp = []

        arrayCargasErrTemp = []

        arrayRaiosTemp = []

        arrayRaiosErrTemp = []

        resultados = [arrayCargasTemp, arrayCargasErrTemp, arrayRaiosTemp, arrayRaiosErrTemp]

        numeroDeRepeticoes = len(self.arrayCargas)

        for i in range(numeroDeRepeticoes):

            # Se o checkBox (que tem o mesmo
            # endereço que o raio e carga
            # de certa gota) não está checkado,
            # o append dessas informações é pulado
            # e a array temporária só vai ter as
            # gotas que estão checkadas
            if self.arrayCheckBoxes[i].isChecked() == True:

                continue

            arrayCargasTemp.append(self.arrayCargas[i])

            arrayRaiosTemp.append(self.arrayRaios[i])

            arrayCargasErrTemp.append(self.arrayErrCargas[i])

            arrayRaiosErrTemp.append(self.arrayErrRaios[i])

        # Essas arrays são requisitadas no plot em si
        return resultados

    #####################
    #####################
    # MÉTODOS DE EDIÇÃO #
    #####################
    #####################

    #####################
    #####################
    # MÉTODOS POPULARES # -> São utilizados por
    #####################    mais de uma janela
    #####################

    # Classificar as velocidades de dada gota i
    def classificarVelocidades(self, dataFrameVelocidades, indice_i):

        i = indice_i

        # Retorna o número de linhas
        quantidadeLinhas = dataFrameVelocidades.shape[0]

        def atribuicaoVelocidadeDescida():

            self.arrayDasArraysVelDes[i].append(velocidade)
            # Tem que se repensar esses appends caso eu
            # deseje possibilitar que o usuário faça a varredura
            """Sinceramente, acho que não seja necessário"""
            self.arrayDasArraysVelDesInstantes[i].append(instante)

        def atribuicaoVelocidadeSubida():

            self.arrayDasArraysVelSub[i].append(velocidade)
            # Tem que se repensar esses appends caso eu
            # deseje possibilitar que o usuário faça a varredura
            """Sinceramente, acho que não seja necessário"""
            self.arrayDasArraysVelSubInstantes[i].append(instante)

        def atribuirVelocidadeDesconsiderada():

            self.arrayDasArraysVelDesconsdrds[i].append(velocidade)
            
            self.arrayDasArraysVelDesconsInsts[i].append(instante)

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

    # Métodos de cálculo de carga e raio de dada gota i
    def calcularCargaRaioGota(self, indice_i):

        i = indice_i

        velDes = self.arrayMediaVelDes[i]

        velSub = self.arrayMediaVelSub[i]

        constante1 = self.constante1

        constante2 = self.constante2

        voltagem = self.voltagem
        
        soma = abs(velDes) + abs(velSub)

        diferenca = abs(velDes) - abs(velSub)

        desvPadAmostMediaVelDes = self.arrayDesvPadAmostMediaVelDes[i]

        desvPadAmostMediaVelSub = self.arrayDesvPadAmostMediaVelSub[i]

        resultados = []

        # Por vezes, aparentemente há gravações que são 
        # feitas além da distância focal
        # da lente, quando isso ocorre a imagem é invertida
        # e o que parece uma gota subindo na verdade é ela caindo.
        # Quem vai atestar bem isso é o fato da velocidade de subida
        # ser maior que a de descida e nesse caso a difença acima irá
        # ser negativa, para corrigir erros de raiz quadrada negativa
        # o melhor é simplesmente inverter a posição dos termos em
        # caso de diferença negativa
        if diferenca < 0:

            diferenca = abs(velSub) - abs(velDes)

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
    
    # Método de classificação de dada gota i
    def classificarGota(self, indice_i):

        i = indice_i

        # Se um dos conjuntos de velocidade tiver
        # menos que 10 itens, é uma gota duvidosa
        if len(self.arrayDasArraysVelDes[i]) < 10 or len(self.arrayDasArraysVelSub[i]) < 10:

            return "Duvidoso"
        
        # Caso um dos conjuntos de velocidade tiver
        # entre 10 e 20 itens, é uma gota razoável
        elif (10 <= len(self.arrayDasArraysVelDes[i]) <= 20) or (10 <= len(self.arrayDasArraysVelSub[i]) <= 20):

            return "Razoável"

        # E caso os dois conjuntos tenham mais
        # de 20 itens, é uma gota confiável
        else:

            return "Confiável"   
        
    # Método responsável pela exibição/
    # atualização do gráfico carga x raio
    def exibirGraficoCarga_Raio(self):

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

        """for line in self.ax.lines:

            line.remove()

        for collection in self.ax.collections:

            collection.remove()

        for patch in self.ax.patches:

            patch.remove()

        if self.ax.get_legend() is not None:

            self.ax.get_legend().remove()"""

        # Note que aqui utiliza a ideia
        # de retornar uma array. O elemento de 
        # endereço 0 retorna a array de cargas 
        # e o endereço 2 retorna a array de raios
        self.ax.errorbar(self.alterarVisibilidadeGota()[2], self.alterarVisibilidadeGota()[0], xerr=self.alterarVisibilidadeGota()[3], yerr=self.alterarVisibilidadeGota()[1], label=f'{self.voltagem} V', color="black", fmt="x", markersize=10, capsize=5)

        # Aumentando a grossura das bordas do gráfico
        self.ax.spines['top'].set_linewidth(2)
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.spines['right'].set_linewidth(2)

        # Aumentando a fonte dos números dos eixos
        self.ax.tick_params(axis='both', labelsize=14)

        # Diminuindo intervalos entre os ticks dos eixos
        """
        Vou deixar em stand-by por enquanto
        self.ax.xaxis.set_major_locator(MultipleLocator(0.01))

        self.ax.yaxis.set_major_locator(MultipleLocator(0.01))"""

        # Colocando os títulos nos eixos
        self.ax.set_xlabel("Raio (m)", fontsize=14)

        self.ax.set_ylabel("Carga (C)", fontsize=14)

        self.ax.legend(fontsize=12)

        self.canvas.draw()

        if not hasattr(self, 'toolbar'):

            self.toolbar = NavigationToolBar(self.canvas, self)

        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.canvas)

    ####################################
    ####################################
    ####################################
    # Recursos que muito provavelmente # 
    # serão utilizados no futuro #######
    ####################################
    ####################################
    ####################################

    """plt.scatter(self.arrayDasArraysVelSubInstantes[i], self.arrayDasArraysVelSub[i], color="red", marker='.')

        plt.scatter(self.arrayDasArraysVelDesInstantes[i], self.arrayDasArraysVelDes[i], color="blue", marker='.')

        plt.plot(dataFrameVelocidades['t'], dataFrameVelocidades['vy'], color='black', linestyle='--')

        plt.title('Velocidade de subida em vermelho e velocidade de descida em azul')
        plt.xlabel('Instante (s)')
        plt.ylabel('Velocidade vertical (m/s)')
        plt.gcf().canvas.manager.set_window_title(f"Velocidade em função do tempo para {arrayNomesTxt[i]}")

        plt.savefig(os.path.join(pastaResultados, f"grafico{arrayNomesTxt[i]}_var{self.varredura}.png"), dpi=300, bbox_inches='tight')

        plt.show()"""
    
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

    #dataFrameEstatisticas = pd.DataFrame(estatisticas)

    #caminho_arquivo_estatisticas = os.path.join(pastaResultados, "estatisticas.csv")

    #dataFrameEstatisticas.to_csv(caminho_arquivo_estatisticas, sep="\t", index=True)

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