import multiprocessing
import time
from selenium import webdriver
import psutil

def abrir_pagina(url):
    # Criar uma nova instância do WebDriver em cada processo
    driver = webdriver.Edge()  # Substitua pelo driver desejado e forneça o caminho correto

    # Abrir a página
    driver.get(url)

    # Monitorar o consumo de memória e CPU
    process = psutil.Process()
    memory_before = process.memory_info().rss
    cpu_percent_before = psutil.cpu_percent(interval=None, percpu=True)

    # Manter a página aberta por um tempo
    time.sleep(10)

    # Fechar o WebDriver
    driver.quit()

    # Monitorar o consumo de memória e CPU após fechar o WebDriver
    memory_after = process.memory_info().rss
    cpu_percent_after = psutil.cpu_percent(interval=None, percpu=True)

    # Obter o número de processadores
    num_processors = psutil.cpu_count()

    # Imprimir os resultados para cada processador
    for i in range(num_processors):
        print(f"  Thread {i+1}:")
        print(f"  Consumo de memória antes: {memory_before} bytes")
        print(f"  Consumo de memória depois: {memory_after} bytes")
        print(f"  Uso de CPU antes: {cpu_percent_before[i]}%")
        print(f"  Uso de CPU depois: {cpu_percent_after[i]}%")
        print()

def multiprocessadores(urls):
    # Criar um pool de processos com o número de processos desejado
    pool = multiprocessing.Pool(processes=2)

    # Mapear a abertura de página para as URLs de entrada
    pool.map(abrir_pagina, urls)

    # Fechar o pool de processos
    pool.close()
    pool.join()

if __name__ == '__main__':
    # URLs de exemplo
    urls = ['https://www.marinetraffic.com', 'https://www.marinetraffic.com']

    multiprocessadores(urls)