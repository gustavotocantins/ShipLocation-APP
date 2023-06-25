import multiprocessing
import time

def processar_dado(dado):
    # Simular algum processamento demorado
    time.sleep(2)
    
    # Retornar o resultado do processamento
    return dado * 2

def multiprocessadores(dados):

    # Criar um pool de processos com o número de processos desejado
    pool = multiprocessing.Pool(processes=5)

    # Mapear o processamento para os dados de entrada e obter os resultados em tempo real
    for resultado in pool.imap(processar_dado, dados):
        print(resultado)

    # Fechar o pool de processos
    pool.close()
    pool.join()

multiprocessadores()
