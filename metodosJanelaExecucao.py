import traceback

import logging

import sys

def capturarExcecao(exctype, value, tb):

    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    print(mensagemErro)

    logging.error(mensagemErro)

if __name__ == __main__:

    sys.excepthook = capturarExcecao

    try:

        pass

    except Exception as e:

        capturarExcecao(*sys.exc_info())

