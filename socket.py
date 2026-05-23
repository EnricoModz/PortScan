import socket
import time
import concurrent.futures

def check_port(host, port):
    try:
        # Cria o socket (IPv4 e TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Timeout curto para a conexão não ficar travada esperando
        s.settimeout(2)
        
        # connect_ex retorna 0 se a porta estiver aberta
        result = s.connect_ex((host, port))
        
        if result == 0:
            banner = "" 
            try:
                # Tenta fazer o banner grabbing (escutar a resposta do servidor por 1 seg)
                s.settimeout(1) 
                
                # Se for HTTP/Proxy, precisamos mandar uma requisição primeiro pra ele falar algo
                if port == 80 or port == 8080:
                    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    
                # Recebe até 1024 bytes e decodifica, ignorando erros e limpando os espaços
                dados = s.recv(1024)
                banner = dados.decode('utf-8', errors='ignore').strip() 
            except:
                # Se der erro ou o servidor não mandar nada, segue o jogo
                pass 
            
            s.close()
            return True, banner 
        else:
            s.close()
            return False, "" 
            
    except socket.error:
        # Em caso de erro na rede, assume que tá fechada
        return False, ""


# Coletando os parâmetros do usuário
IP = input("Digite o IP alvo: ")
host = IP
porta_limite = int(input("Digite até qual porta deseja escanear: "))

total_abertas = 0
total_fechadas = 0

tempo_inicio = time.time()

# Abre o arquivo no modo "a" (append) para adicionar no final sem apagar o histórico
with open("relatorio_varredura.txt", "a", encoding="utf-8") as arquivo:
    # Coloquei uns \n\n no começo para dar um espaço entre o relatório antigo e esse novo!
    arquivo.write(f"\n\n=== NOVO RELATÓRIO DE VARREDURA ===\n")
    arquivo.write(f"Alvo Escaneado: {host}\n")
    arquivo.write(f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    arquivo.write(f"----------------------------------------\n\n")
    arquivo.write(f"Alvo Escaneado: {host}\n")
    arquivo.write(f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    arquivo.write(f"----------------------------------------\n\n")

# Inicia o pool de threads pra fazer o scan voar (50 portas por vez)
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    
    # Mapeia as execuções (future) com o número da porta
    futures = {executor.submit(check_port, host, port): port for port in range(1, porta_limite + 1)}

    # Processa os resultados conforme as threads vão terminando
    for future in concurrent.futures.as_completed(futures):
        port = futures[future] 
        status_aberta, banner = future.result() 
        
        if status_aberta == True:
            # Tenta descobrir o serviço associado à porta via SO
            try:
                nome_servico = socket.getservbyport(port, "tcp")
            except Exception:
                # Fallback: dicionário próprio se o SO não reconhecer a porta
                portas_conhecidas = {
                    21: "ftp", 22: "ssh", 53: "dns", 80: "http", 
                    110: "pop3", 143: "imap", 443: "https", 
                    3306: "mysql", 8080: "http-proxy"
                }
                nome_servico = portas_conhecidas.get(port, "Desconhecido")
            
            # Formata a string de saída dependendo se capturou um banner ou não
            if banner != "":
                mensagem_porta = f"Porta {port} ABERTA - Serviço: {nome_servico} | Banner: {banner}"
            else:
                mensagem_porta = f"Porta {port} ABERTA - Serviço: {nome_servico}"
                
            # Printa na tela em tempo real
            print(mensagem_porta)
            
            # Salva no arquivo (usando 'a' de append pra não apagar o que já foi salvo)
            with open("relatorio_varredura.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(mensagem_porta + "\n")
                
            total_abertas += 1  
        else:
            total_fechadas += 1

tempo_fim = time.time()
tempo_execucao = tempo_fim - tempo_inicio

# Monta o bloco de resumo final
resumo = f"\n----------------------------------------\n"
resumo += f"=== RESUMO FINAL ===\n"
resumo += f"Total de portas abertas: {total_abertas}\n"
resumo += f"Total de portas fechadas: {total_fechadas}\n"
resumo += f"Tempo total de execução: {tempo_execucao:.2f} segundos\n"

# Exibe o resumo e também anexa no fim do arquivo txt
print(resumo)
with open("relatorio_varredura.txt", "a", encoding="utf-8") as arquivo:
    arquivo.write(resumo)
