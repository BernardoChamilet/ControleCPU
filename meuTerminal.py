#Grupo: Bernardo Boggione Chamilet (155564) e Rafaella Masutti Rodrigues (155567)

import psutil
import time

# Obtém cota de tempo de CPU em segundos
tempoCPU = float(input("Digite a cota de tempo de CPU em segundos: "))
# Obtém o tempo limite de relógio para execução de um programa em segundos
tempoLimite = float(input("Digite o tempo limite de execução de um programa em segundos: ")) 
while True:
    # Obtém binário a ser executado
    strBinario = input("Digite o programa que gostaria de executar (ou sair para sair): ")
    if strBinario == "sair":
        print("Tchau")
        break
    # Cria um processo para o binário informado
    processo = psutil.Popen([strBinario])
    tempoInicial = time.time()
    tempoCPUanterior = 0.0
    while True:
        # Programa foi encerrado manualmente
        if processo.is_running() == False:
            # Calculo do tempo de relógio restante que tinha
            tempoRestante = tempoLimite - (time.time() - tempoInicial)
            break
        else:
            # obtendo tempo gasto de CPU até o momento
            try:
                # lógica para detectar mudanças no tempo de cpu
                # caso haja mudanças subtraímos o uso da cpu da cota total
                # assim enquanto o programa roda controlamos o tempo de cpu
                # encerrando o programa quando a cota acabar :)
                # Calculando tempo de CPU usado e restante
                temposCPU = processo.cpu_times()
                tempoUser = temposCPU.user
                tempoSystem = temposCPU.system
                tempoTotal = tempoUser + tempoSystem
                # verificando mudança no tempo de cpu
                diferencaTempos = tempoTotal - tempoCPUanterior
                if diferencaTempos != 0:
                    tempoCPU = tempoCPU - diferencaTempos
                    if tempoCPU <= 0:
                        processo.kill()
                        break
                tempoCPUanterior = tempoTotal
            except:
                print("Segue a vida")
            # tempo de relógio esgotado
            if time.time() >= tempoInicial + tempoLimite:
                tempoRestante = 0
                processo.kill()
                break
    print("Tempo de CPU usado até o momento:") 
    print(f"{tempoUser} segundos (user) + {tempoSystem} segundos (sistema) totalizando {tempoTotal} segundos.")
    print(f"Você tem {tempoCPU} segundos de CPU restantes")
    # Caso tempo de CPU foi esgotado
    if tempoCPU <= 0:
        print("Acabou o tempo de CPU. Obrigado por usar nosso terminal")
        print("Até mais!")
        break
    # Caso tempo de relógio foi esgotado ou não
    if tempoRestante == 0:
        print("Acabou o tempo de rodar esse programa")
    else:
        print(f"Você ainda tinha {tempoRestante} segundos para usar")