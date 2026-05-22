import socket
import time
import concurrent.futures

def check_port(host, port):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((host, port))
    s.close()
    if result == 0:
      return True
    else:
      return False
  except socket.error:
    return False 

IP = input("Digite o IP: ")
host = IP

porta_limite = int(input("Digite a porta máxima: "))

total_abertas = 0
total_fechadas = 0

tempo_inicio = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
  futures = {executor.submit(check_port, host, port): port for port in range(1, porta_limite + 1)}

  for future in concurrent.futures.as_completed(futures):
      port = futures[future] 
      result = future.result() 
    
      if result:
        # 1. Tenta descobrir o nome do serviço
          try:
              nome_servico = socket.getservbyport(port, "tcp")
          except:
            # Se a porta for um número aleatório que não está no padrão (ex: 9999)
            # o Python dá erro. O except captura esse erro e chamamos de Desconhecido.
              nome_servico = "Desconhecido"
            
        # 2. Agora imprimimos a mensagem já com o nome do serviço no final!
          print(f"Porta {port} ABERTA em {host} - Serviço: {nome_servico}")
          total_abertas += 1  
      else:
        total_fechadas += 1

tempo_fim = time.time()

print("--- RESUMO DA VARREDURA ---")
print(f"Total de portas abertas: {total_abertas}")
print(f"Total de portas fechadas: {total_fechadas}")

tempo_execucao = tempo_fim - tempo_inicio
print(f"A varredura demorou = {tempo_execucao:.2f} segundos")
